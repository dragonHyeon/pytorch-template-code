class Tester:
    def __init__(self, model, loss_fn, metric_fn, test_dataloader, device):
        """
        * 테스트 관련 클래스
        :param model: 테스트 할 모델
        :param loss_fn: 손실 함수
        :param metric_fn: 학습 성능 체크하기 위한 metric
        :param test_dataloader: 테스트용 데이터로더
        :param device: GPU / CPU
        """

        # 테스트 할 모델
        self.model = model
        # 손실 함수
        self.loss_fn = loss_fn
        # 학습 성능 체크하기 위한 metric
        self.metric_fn = metric_fn
        # 테스트용 데이터로더
        self.test_dataloader = test_dataloader
        # GPU / CPU
        self.device = device

    def running(self):
        """
        *
        :return:
        """

        # 테스트 진행
        self._test()

    def _test(self):
        """
        * 테스트 진행
        :return:
        """

        pass
