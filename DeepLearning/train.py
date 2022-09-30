from copy import deepcopy

from Common import ConstVar
from Lib import UtilLib
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

    def running(self, num_epoch, save_dir, Tester, test_dataloader, metric_fn, checkpoint_file=None):
        """
        *
        :param num_epoch: 학습 반복 횟수
        :param save_dir: 체크포인트 파일 저장할 디렉터리 위치
        :param Tester: 학습 성능 체크하기 위한 테스트 관련 클래스
        :param test_dataloader: 학습 성능 체크하기 위한 테스트용 데이터로더
        :param metric_fn: 학습 성능 체크하기 위한 metric
        :param checkpoint_file: 불러올 체크포인트 파일
        :return:
        """

        # epoch 초기화
        start_epoch_num = ConstVar.INITIAL_START_EPOCH_NUM

        # 불러올 체크포인트 파일 있을 경우 불러오기
        if checkpoint_file:
            state = utils.load_checkpoint(filepath=checkpoint_file)
            self.model.load_state_dict(state[ConstVar.KEY_STATE_MODEL])
            self.model.to(self.device)
            self.optimizer.load_state_dict(state[ConstVar.KEY_STATE_OPTIMIZER])

            start_epoch_num = state[ConstVar.KEY_STATE_EPOCH] + 1

        # num epoch 만큼 학습 반복
        for current_epoch_num, _ in enumerate(range(num_epoch), start=start_epoch_num):

            # 학습 진행
            self._train()

            # 학습 진행 저장
            utils.save_checkpoint(filepath=UtilLib.getNewPath(path=save_dir,
                                                              add=ConstVar.CHECKPOINT_FILE_NAME.format(current_epoch_num)),
                                  model=self.model,
                                  optimizer=self.optimizer,
                                  epoch=current_epoch_num,)
                                  # is_best=self._check_is_best(tester=Tester(model=deepcopy(x=self.model),
                                  #                                           loss_fn=self.loss_fn,
                                  #                                           metric_fn=metric_fn,
                                  #                                           test_dataloader=test_dataloader,
                                  #                                           device=self.device)))

    def _train(self):
        """
        * 학습 진행
        :return: 1 epoch 만큼 학습 진행
        """

        # 모델을 학습 모드로 전환
        self.model.train()

        # 모델을 해당 디바이스로 이동
        self.model.to(self.device)

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

    def _check_is_best(self, tester):
        """
        * 현재 저장하려는 모델이 가장 좋은 성능의 모델인지 여부 확인
        :param tester: 현재 모델의 성능을 테스트하기 위한 테스트 객체
        :return: True / False
        """

        # 현재 모델로 테스트 진행
        tester.running()

        # best 성능 갱신
        if tester.score < self.best_score:
            self.best_score = tester.score
            return True
        else:
            return False
