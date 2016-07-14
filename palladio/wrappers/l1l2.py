import l1l2py

import numpy as np

from l1l2signature import utils as l1l2_utils

class l1l2Classifier:

    def __init__(self, params):

        self._params = params

    def setup(self, Xtr, Ytr, Xts, Yts):

        self._Xtr = Xtr
        self._Ytr = Ytr

        self._Xts = Xts
        self._Yts = Yts

        rs = l1l2_utils.RangesScaler(Xtr, Ytr,
                                     self._params['data_normalizer'],
                                     self._params['labels_normalizer'])

        self._tau_range = rs.tau_range(self._params['tau_range'])
        self._mu_range = rs.mu_range(np.array([self._params['mu']]))
        self._lambda_range = np.sort(self._params['lambda_range'])

        pass

    def run(self):

        # Execution
        result = l1l2py.model_selection(
            self._Xtr, self._Ytr, self._Xts, self._Yts,
            self._mu_range, self._tau_range, self._lambda_range,
            self._params['ms_split'], self._params['cv_error'], self._params['error'],
            self._params['data_normalizer'], self._params['labels_normalizer'],
            self._params['sparse'], self._params['regularized'], self._params['return_predictions']
            )

        ### Return only the first element of the list, which is the one related to the smallest value of mu
        ### BEGIN
        result['selected_list'] = result['selected_list'][0]
        result['beta_list'] = result['beta_list'][0]

        result['prediction_ts_list'] = result['prediction_ts_list'][0].ravel()
        if 'prediction_tr_list' in result.keys():
            result['prediction_tr_list'] = result['prediction_tr_list'][0].ravel()

        ### END


        return result


    pass
