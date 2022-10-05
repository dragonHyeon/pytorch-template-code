import torch
from torch.utils.data import DataLoader

from Common import ConstVar
from DeepLearning.train import Trainer
from DeepLearning.test import Tester
from DeepLearning.dataloader import SIGNSDataset
from DeepLearning.model import LeNet
from DeepLearning.loss import loss_fn
from DeepLearning.metric import accuracy


def run(args):
    """
    * 실행 코드
    :param args:
    :return:
    """

    # GPU / CPU 설정
    device = ConstVar.DEVICE_CUDA if torch.cuda.is_available() else ConstVar.DEVICE_CPU

    # 학습 모드
    if args.mode_train_test == ConstVar.MODE_TRAIN:

        # 모델 선언
        model = LeNet()
        # 모델을 해당 디바이스로 이동
        model.to(device)

        # optimizer 선언
        optimizer = torch.optim.Adagrad(params=model.parameters(),
                                        lr=args.learning_rate)

        # 학습용 데이터로더 선언
        train_dataloader = DataLoader(dataset=SIGNSDataset(data_dir=args.data_dir,
                                                           mode_train_test=ConstVar.MODE_TRAIN),
                                      batch_size=args.batch_size,
                                      shuffle=args.shuffle)

        # 테스트용 데이터로더 선언
        test_dataloader = DataLoader(dataset=SIGNSDataset(data_dir=args.data_dir,
                                                          mode_train_test=ConstVar.MODE_TEST),
                                     batch_size=args.batch_size,
                                     shuffle=args.shuffle)

        # 모델 학습 객체 선언
        trainer = Trainer(model=model,
                          optimizer=optimizer,
                          loss_fn=loss_fn,
                          train_dataloader=train_dataloader,
                          device=device)

        # 모델 학습
        trainer.running(num_epoch=args.num_epoch,
                        save_dir=args.save_dir,
                        Tester=Tester,
                        test_dataloader=test_dataloader,
                        metric_fn=accuracy,
                        checkpoint_file=args.checkpoint_file)

    # 테스트 모드
    elif args.mode_train_test == ConstVar.MODE_TEST:

        # 모델 선언
        model = LeNet()
        # 모델을 해당 디바이스로 이동
        model.to(device)

        # 테스트용 데이터로더 선언
        test_dataloader = DataLoader(dataset=SIGNSDataset(data_dir=args.data_dir,
                                                          mode_train_test=ConstVar.MODE_TEST),
                                     batch_size=args.batch_size,
                                     shuffle=args.shuffle)

        # 모델 테스트 객체 선언
        tester = Tester(model=model,
                        metric_fn=accuracy,
                        test_dataloader=test_dataloader,
                        device=device)

        # 모델 테스트
        tester.running()
