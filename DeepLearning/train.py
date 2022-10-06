from copy import deepcopy

from Common import ConstVar
from Lib import UtilLib, DragonLib
from DeepLearning import utils


class Trainer:
    def __init__(self, model, optimizer, loss_fn, train_dataloader, device):
        """
        * 학습 관련 클래스
        :param model: 학습 시킬 모델
        :param optimizer: 학습 optimizer
        :param loss_fn: 손실 함수
        :param train_dataloader: 학습용 데이터로더
        :param device: GPU / CPU
        """

        # 학습 시킬 모델
        self.model = model
        # 학습 optimizer
        self.optimizer = optimizer
        # 손실 함수
        self.loss_fn = loss_fn
        # 학습용 데이터로더
        self.train_dataloader = train_dataloader
        # GPU / CPU
        self.device = device

    def running(self, num_epoch, save_dir, save_frequency, Tester, test_dataloader, metric_fn, checkpoint_file=None):
        """
        * 학습 셋팅 및 진행
        :param num_epoch: 학습 반복 횟수
        :param save_dir: 체크포인트 파일 저장할 디렉터리 위치
        :param save_frequency: 체크포인트 파일 저장 빈도수
        :param Tester: 학습 성능 체크하기 위한 테스트 관련 클래스
        :param test_dataloader: 학습 성능 체크하기 위한 테스트용 데이터로더
        :param metric_fn: 학습 성능 체크하기 위한 metric
        :param checkpoint_file: 불러올 체크포인트 파일
        :return: 학습 완료 및 체크포인트 파일 생성됨
        """

        # epoch 초기화
        start_epoch_num = ConstVar.INITIAL_START_EPOCH_NUM

        # 불러올 체크포인트 파일 있을 경우 불러오기
        if checkpoint_file:
            state = utils.load_checkpoint(filepath=checkpoint_file)
            self.model.load_state_dict(state[ConstVar.KEY_STATE_MODEL])
            self.optimizer.load_state_dict(state[ConstVar.KEY_STATE_OPTIMIZER])
            start_epoch_num = state[ConstVar.KEY_STATE_EPOCH] + 1

        # num epoch 만큼 학습 반복
        for current_epoch_num, count in enumerate(range(num_epoch), start=start_epoch_num):

            # 학습 진행
            self._train()

            # 체크포인트 저장 주기마다 학습 진행 저장
            if (count + 1) % save_frequency == 0:
                filepath = UtilLib.getNewPath(path=save_dir,
                                              add=ConstVar.CHECKPOINT_FILE_NAME.format(current_epoch_num))
                DragonLib.make_parent_dir_if_not_exits(target_path=filepath)
                utils.save_checkpoint(filepath=filepath,
                                      model=self.model,
                                      optimizer=self.optimizer,
                                      epoch=current_epoch_num,
                                      is_best=self._check_is_best(tester=Tester(model=deepcopy(x=self.model),
                                                                                metric_fn=metric_fn,
                                                                                test_dataloader=test_dataloader,
                                                                                device=self.device),
                                                                  best_checkpoint_dir=save_dir))

    def _train(self):
        """
        * 학습 진행
        :return: 1 epoch 만큼 학습 진행
        """

        # 모델을 학습 모드로 전환
        self.model.train()

        # x shape: (N, 3, 32, 32)
        # y shape: (N)
        for x, y in self.train_dataloader:

            # 각 텐서를 해당 디바이스로 이동
            x = x.to(self.device)
            y = y.to(self.device)

            # 순전파
            y_pred = self.model(x)
            loss = self.loss_fn(y_pred, y)

            # 역전파
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

    def _check_is_best(self, tester, best_checkpoint_dir):
        """
        * 현재 저장하려는 모델이 가장 좋은 성능의 모델인지 여부 확인
        :param tester: 현재 모델의 성능을 테스트하기 위한 테스트 객체
        :param best_checkpoint_dir: 비교할 best 체크포인트 파일 디렉터리 위치
        :return: True / False
        """

        # 현재 모델로 테스트 진행
        tester.running()
        current_score = tester.score

        # best 성능 측정을 위해 초기화
        try:
            self.best_score
        except AttributeError:
            checkpoint_file = UtilLib.getNewPath(path=best_checkpoint_dir,
                                                 add=ConstVar.CHECKPOINT_BEST_FILE_NAME)
            # 기존에 측정한 best 체크포인트가 있으면 해당 score 로 초기화
            if UtilLib.isExist(checkpoint_file):
                tester.running(checkpoint_file=checkpoint_file)
                self.best_score = tester.score
            # 없다면 0 으로 초기화
            else:
                self.best_score = ConstVar.INITIAL_BEST_ACCURACY_ZERO

        # best 성능 갱신
        if current_score > self.best_score:
            self.best_score = current_score
            return True
        else:
            return False
