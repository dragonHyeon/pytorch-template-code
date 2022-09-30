import torch
from torch.utils.data import DataLoader

from Common import ConstVar
from DeepLearning.model import LeNet
from DeepLearning.dataloader import SIGNSDataset
from DeepLearning.train import Trainer
from DeepLearning.test import Tester
from DeepLearning.loss import loss_fn


def run(args):
    """
    * 실행 코드
    :param args:
    :return:
    """

    # GPU / CPU 설정
    device = ConstVar.DEVICE_CUDA if torch.cuda.is_available() else ConstVar.DEVICE_CPU

    # 모델 선언
    model = LeNet()

    # 학습 모드
    if args.mode_train_test == ConstVar.MODE_TRAIN:

        # optimizer 선언
        optimizer = torch.optim.Adam(params=model.parameters(),
                                     lr=ConstVar.LEARNING_RATE)

        # 학습용 데이터로더 선언
        train_dataloader = DataLoader(dataset=SIGNSDataset(data_dir=ConstVar.DATA_DIR_TRAIN,
                                                           mode_train_test=ConstVar.MODE_TRAIN),
                                      batch_size=ConstVar.BATCH_SIZE,
                                      shuffle=ConstVar.SHUFFLE)

        # 모델 학습 객체 선언
        trainer = Trainer(model=model,
                          optimizer=optimizer,
                          loss_fn=loss_fn,
                          train_dataloader=train_dataloader,
                          device=device)

        # 모델 학습
        trainer.running(num_epoch=ConstVar.NUM_EPOCH,
                        save_dir='.',
                        Tester=Tester,
                        test_dataloader=train_dataloader,
                        metric_fn=1,
                        checkpoint_file='../Main/epoch00001.ckpt')

    # 테스트 모드
    elif args.mode_train_test == ConstVar.MODE_TEST:

        # 테스트용 데이터로더 선언
        test_dataloader = DataLoader(dataset=SIGNSDataset(data_dir=ConstVar.DATA_DIR_TEST,
                                                          mode_train_test=ConstVar.MODE_TEST),
                                     batch_size=ConstVar.BATCH_SIZE,
                                     shuffle=ConstVar.SHUFFLE)

        # 모델 테스트 객체 선언
        tester = Tester(model=model,
                        loss_fn=loss_fn,
                        test_dataloader=test_dataloader,
                        device=device)

        # 모델 테스트
        tester.running()
