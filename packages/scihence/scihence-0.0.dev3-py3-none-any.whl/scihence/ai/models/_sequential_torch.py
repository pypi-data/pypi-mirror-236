"""Sequential PyTorch models."""
import torch
from torch import Tensor, nn

from scihence.ai._io import DaitaFraime
from scihence.ai.models._torch import (
    BaseTorchClassificationModel,
    BaseTorchRegressionModel,
    Linear3D,
    pre_post_process,
)


class TorchRNNSequenceRegressor(BaseTorchRegressionModel):

    def __init__(self, n_outputs, **kwargs) -> None:
        super().__init__(**kwargs)
        self.rnn = nn.RNN(input_size=10, hidden_size=6, num_layers=4, batch_first=True)
        self.lstm = nn.LSTM(input_size=6, hidden_size=5, num_layers=2, batch_first=True)
        self.dense = nn.Linear(5, n_outputs)

    @pre_post_process
    def forward(self, X: DaitaFraime) -> list[Tensor]:
        X, sequence_lens = X.to_torch(), X.sequence_lens
        X = nn.utils.rnn.pad_sequence(X, batch_first=True)
        X = nn.utils.rnn.pack_padded_sequence(
            X, lengths=sequence_lens, enforce_sorted=False, batch_first=True
        )
        X, _ = self.rnn(X)
        X, _ = self.lstm(X)
        X, _ = nn.utils.rnn.pad_packed_sequence(X, batch_first=True)
        X = self.dense(X[:, -1])
        return X


class TorchRNNSequenceToSequenceRegressor(BaseTorchRegressionModel):

    def __init__(self, n_outputs, **kwargs) -> None:
        super().__init__(**kwargs)
        self.rnn = nn.RNN(input_size=10, hidden_size=6, num_layers=4, batch_first=True)
        self.lstm = nn.LSTM(input_size=6, hidden_size=5, num_layers=2, batch_first=True)
        self.dense = nn.Linear(5, n_outputs)

    @pre_post_process
    def forward(self, X: DaitaFraime) -> list[Tensor]:
        X, sequence_lens = X.to_torch(), X.sequence_lens
        X = nn.utils.rnn.pad_sequence(X, batch_first=True)
        X = nn.utils.rnn.pack_padded_sequence(
            X, lengths=sequence_lens, enforce_sorted=False, batch_first=True)
        X, _ = self.rnn(X)
        X, _ = self.lstm(X)
        X, _ = nn.utils.rnn.pad_packed_sequence(X, batch_first=True)
        X = [sequence[:sequence_len] for sequence, sequence_len in zip(X, sequence_lens)]
        X = self.dense(torch.cat(X))
        X = list(torch.split(X, sequence_lens.to_list()))
        return X


class TorchRNNSequenceClassifier(BaseTorchClassificationModel):

    def __init__(self, n_outputs, n_classes, **kwargs) -> None:
        super().__init__(**kwargs)
        self.rnn = nn.RNN(input_size=10, hidden_size=6, num_layers=4, batch_first=True)
        self.lstm = nn.LSTM(input_size=6, hidden_size=5, num_layers=2, batch_first=True)
        self.dense = Linear3D(n_features=5, n_outputs=n_outputs, n_classes=n_classes)

    @pre_post_process
    def forward(self, X: DaitaFraime) -> list[Tensor]:
        X, sequence_lens = X.to_torch(), X.sequence_lens
        X = nn.utils.rnn.pad_sequence(X, batch_first=True)
        X = nn.utils.rnn.pack_padded_sequence(
            X, lengths=sequence_lens, enforce_sorted=False, batch_first=True)
        X, _ = self.rnn(X)
        X, _ = self.lstm(X)
        X, _ = nn.utils.rnn.pad_packed_sequence(X, batch_first=True)
        X = self.dense(X[:, -1])
        return X


class TorchRNNSequenceToSequenceClassifier(BaseTorchClassificationModel):

    def __init__(self, n_outputs, n_classes, **kwargs) -> None:
        super().__init__(**kwargs)
        self.rnn = nn.RNN(input_size=10, hidden_size=6, num_layers=4, batch_first=True)
        self.lstm = nn.LSTM(input_size=6, hidden_size=5, num_layers=2, batch_first=True)
        self.dense = Linear3D(n_features=5, n_outputs=n_outputs, n_classes=n_classes)

    @pre_post_process
    def forward(self, X: DaitaFraime) -> list[Tensor]:
        X, sequence_lens = X.to_torch(), X.sequence_lens
        X = nn.utils.rnn.pad_sequence(X, batch_first=True)
        X = nn.utils.rnn.pack_padded_sequence(
            X, lengths=sequence_lens, enforce_sorted=False, batch_first=True)
        X, _ = self.rnn(X)
        X, _ = self.lstm(X)
        X, _ = nn.utils.rnn.pad_packed_sequence(X, batch_first=True)
        X = [sequence[:sequence_len] for sequence, sequence_len in zip(X, sequence_lens)]
        X = self.dense(torch.cat(X))
        X = list(torch.split(X, sequence_lens.to_list()))
        return X
