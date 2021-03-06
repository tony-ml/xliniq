from base import *
from ml.mini_batch_relu_latent_factor_model import MiniBatchReLuLatentFactorModel
from ml.mse_tester import MseTester
from ml.average_precision_k_tester import AveragePrecisionKTester
from ml.data_set_splitter import DataSetSplitter
import pickle


def train_test(dataset: str, params: dict):
    print(f"train and test using {params}")
    sds_file_path = f'./output/{dataset}.sds'
    save_name = f"model{'_'.join(map(str, params.values()))}"
    model = MiniBatchReLuLatentFactorModel(**params)

    R = DataSetSplitter.get_train_utility_matrix(sds_file_path)
    model.train(R)

    VAL = DataSetSplitter.get_validate_utility_matrix(sds_file_path)
    mset = MseTester(model)
    mse = mset(VAL)
    print(mse)
    apkt = AveragePrecisionKTester(model)
    apk = apkt(VAL)
    print(apk)

    with open(f'./output/{save_name}.pickle', 'wb') as f:
        pickle.dump(model, f)


if __name__ == '__main__':
    dataset = 'AllPublicXML'
    params = {
        'tau': -1e-3, 'k': 1e3, 'lambda_': 0.01, 'alpha': 0.1, 'max_epoch': 60,
    }
    train_test(dataset, params)
