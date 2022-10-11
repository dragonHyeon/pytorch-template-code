import torch.nn as nn


class AlexNet(nn.Module):
    def __init__(self):
        super(AlexNet, self).__init__()

    def forward(self, x):
        pass


class LeNet(nn.Module):
    def __init__(self):
        """
        * 모델 구조 정의
        """

        super(LeNet, self).__init__()

        self.conv1 = nn.Conv2d(in_channels=3, out_channels=6, kernel_size=5, stride=1, padding=0)
        self.tanh1 = nn.Tanh()
        self.avg_pool1 = nn.AvgPool2d(kernel_size=2, stride=2, padding=0)
        self.conv2 = nn.Conv2d(in_channels=6, out_channels=16, kernel_size=5, stride=1, padding=0)
        self.tanh2 = nn.Tanh()
        self.avg_pool2 = nn.AvgPool2d(kernel_size=2, stride=2, padding=0)
        self.conv3 = nn.Conv2d(in_channels=16, out_channels=120, kernel_size=5, stride=1, padding=0)
        self.fc1 = nn.Linear(in_features=120, out_features=84)
        self.fc2 = nn.Linear(in_features=84, out_features=6)

    def forward(self,x):
        """
        * 순전파
        :param x: 배치 개수 만큼의 입력
        :return: 배치 개수 만큼의 출력
        """

        # (N, 3, 32, 32) -> (N, 6, 28, 28)
        x = self.conv1(x)
        x = self.tanh1(x)
        # (N, 6, 28, 28) -> (N, 6, 14, 14)
        x = self.avg_pool1(x)
        # (N, 6, 14, 14) -> (N, 16, 10, 10)
        x = self.conv2(x)
        x = self.tanh2(x)
        # (N, 16, 10, 10) -> (N, 16, 5, 5)
        x = self.avg_pool2(x)
        # (N, 16, 5, 5) -> (N, 120, 1, 1)
        x = self.conv3(x)
        # (N, 120, 1, 1) -> (N, 120)
        x = x.view(-1, 120)
        # (N, 120) -> (N, 84)
        x = self.fc1(x)
        # (N, 84) -> (N, 6)
        x = self.fc2(x)

        return x
