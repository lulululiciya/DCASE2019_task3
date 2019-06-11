import yaml
import numpy as np
import time
import subprocess
import sys

"""
script to schedule a plan of jobs for a specific model, including:
-N trials of the experiment (to average scores and report more consistently)
-trying with some different parameters for analysis

from this script, we edit a config/params_file.yaml, and call a main script
Then, the main script loads all the params from yaml and runs the experiment
"""

# ---------
start = time.time()

# output_file = 'debug_trial'

# nb of trials in the experiment
N = 1

# params to try************************************
# basic params by default
# lr=0.001 in Adam this is the default
# lrs = [0.0001]
# batch_sizes = [100]
# mode_last_patch = 'fill'  # fill was found to be better!!

# explore the main params of the net, plus patch_len
# patch_lens = [25, 50, 75, 100]
# cnn_nb_filts = [64, 128]
# rnn_nbs = [[32], [64], [128]]
# fc_nbs = [[16], [32], [64]]
# dropout_rate = 0.5  # this was found to be VERY important. Always include

# output_file = 'crnn_seld_explore_net_params_NOdropout'
# output_file = 'crnn_seld_explore_net_params_YESdropout'
# output_file = 'crnn_seld_explore_net_params_03dropout'

# output_file = 'crnn_seld_explore_net_params_YESdropout_fill'
# mode_last_patch = 'fill'

# output_file = 'crnn_seld_explore_net_params_YESdropout_RNNx2'
# rnn_nbs = [[32, 32], [64, 64], [128, 128]]      # this is the way to encode 2 layers
# rnn_nbs = [[32], [64], [128]]      # this is the way to encode 1 layers. it must always be a list of things
# refine
# output_file = 'crnn_seld_explore_net_params_YESdropout_RNNx2'
# output_file = 'crnn_seld_explore_net_params_YESdropout_RNNx2_refine_cnn128_rnn64_fc32_check_patchLen'
# cnn_nb_filts = [128]
# rnn_nbs = [[64, 64]]      # this is the way to encode 2 layers
# fc_nbs = [[32]]
# models = ['crnn_seld']


# output_file = 'crnn_seld_explore_net_params_YESdropout_tagger_head'
# output_file = 'crnn_seld_explore_net_params_YESdropout_tagger_head_Dense_layer_more'
# output_file = 'crnn_seld_explore_net_params_YESdropout_tagger_head_GRU_layer_more'
# models = ['crnn_seld_tagger']
# fc_nbs = [[32], [64]]
# rnn_nbs = [[32, 32], [64, 64]]      # this is the way to encode 2 layers
# fc_nbs = None
# output_file = 'crnn_seld_explore_net_params_YESdropout_tagger_head_Dense_layer_more64_coded_inyaml' # no está claro que ayuda mucho, quizá solo un poco
# patch_lens = [50, 75, 100]   # to start in


#
# models = ['crnn_seld_tagger']
# patch_lens = [50, 75, 100]   # to start in
# output_file = 'crnn_seld_explore_net_params_YESdropout_tagger_head_Dense_layer_more32_coded_inyaml_withFORGOTTEN_BN' meterla no ayuda

# output_file = 'crnn_seld_explore_net_params_YESdropout_tagger_head_Dense_layer_more32_coded_inyaml_preact' MAL

# output_file = 'crnn_seld_explore_net_params_YESdropout_tagger_head_Dense_layer_more32_coded_inyaml_audiovarup1s' MAL


# June 2nd---------------------------------------------------------------------------------------------
# lrs = [0.0001]    # this one yields slighly lower results, but nicer curves. allows for more capacity in FC or CNN
# lrs = [0.001]   # this one yields a bit better results, but closer to OF. DANGER, architecture BETA
batch_sizes = [100]
patch_lens = [50]
mode_last_patch = 'fill'  # fill was found to be better!!
models = ['crnn_seld_tagger']
cnn_nb_filts = [64, 128]
rnn_nbs = [[64], [128]]
dropout_rate = 0.5  # this was found to be VERY important. Always include


# trying with the lr of Keras by default (same used by SA in SELD and SED
# lrs = [0.001]
# output_file = 'crnn_seld_explore_net_params_YESdropout_tagger_head_Dense_layer_more32_coded_inyaml_lr0.001'

# trying with other batchsizes. SA usees 128 in SED, 16 in SELD
# batch_sizes = [64, 128]
# output_file = 'crnn_seld_explore_net_params_YESdropout_tagger_head_Dense_layer_more32_coded_inyaml_batch_64_128'

# cnn_nb_kernelsizes = [(5, 5), (5, 3), (7, 3), (3, 5), (3, 7), (7, 7)]
# cnn_nb_filts = [128]
# rnn_nbs = [[64]]
# output_file = 'crnn_seld_explore_net_params_YESdropout_tagger_head_Dense_layer_more32_coded_inyaml_kernelsizes_oknow'



# ===================================================vip archi  ALPHA, with lrs = [0.0001]
# lrs = [0.0001]    # this one yields slighly lower results, but nicer curves. allows for more capacity in FC or CNN
# cnn_nb_filts = [128]
# rnn_nbs = [[64]]
# fc_nbs = [[32]]
# # output_file = 'crnn_seld_explore_net_tagger_ALPHA'
# n_mels = [128]


# ===================================================vip archi BETA, with lrs = [0.001]
cnn_nb_filts = [64]
rnn_nbs = [[64]]
fc_nbs = [[32]]
# output_file = 'crnn_seld_explore_net_tagger_BETA'
n_mels = [64]
lrs = [0.001]   # this one yields a bit better results, but closer to OF. DANGER, architecture BETA
# lrs = [0.0005]   # this one we never tried


# ===============================================================
# output_file = 'crnn_seld_explore_net_tagger_ALPHA_nmels'
# output_file = 'crnn_seld_Q_explore_net_tagger_ALPHA_nmels'
# n_mels = [40, 64, 96, 128]
# n_mels = [64, 96, 128]

# output_file = 'crnn_seld_explore_net_tagger_BETA_nmels'
# output_file = 'crnn_seld_Q_explore_net_tagger_BETA_nmels'
# n_mels = [40, 64, 96, 128]
# n_mels = [64, 96, 128]


# ************************************************************************************ mixup
enable_mixup_warmup = 0   # this to 0 means enable warmup, must be changed below in data['learn']['stages']
# so I leave it always here, but the Enable is below in data['learn']['stages']
mixup_mode = 'intra'
mixup_log = False
mixup_clamp = False
mixup_warmup_epochs = [-1]
# mixup_alphas = [0.1, 0.2, 0.3, 0.4, 1, 2, 4]
# mixup_alphas = [0.05, 0.1, 0.15, 0.2]
# output_file = 'crnn_seld_Q_explore_net_tagger_BETA_mixup_alpha'
# output_file = 'crnn_seld_Q_explore_net_tagger_BETA64_lr0.001_mixup_alpha_05101520'
# output_file = 'crnn_seld_Q_explore_net_tagger_BETA64_lr0.0005_mixup_alpha_05101520'
# output_file = 'crnn_seld_Q_explore_net_tagger_ALPHA128_lr0.0001_mixup_alpha_05101520'

# ********************************************************submission over the evaluation set
# output_file = 'crnn_seld_Q_explore_net_tagger_SUBMIT_EVAL_SET_v0' # train with splits  [3, 4, 2]
output_file = 'crnn_seld_Q_explore_net_tagger_SUBMIT_EVAL_SET_v1'   # train with splits  [1, 2, 3]
mixup_alphas = [0.1]


# output_file = 'crnn_seld_Q_explore_net_tagger_BETA_mixup_warmup'
# # # to enable warmup, must change below in data['learn']['stages']
# mixup_warmup_epochs = [4, 8]
# mixup_alphas = [0.1, 0.2, 0.3, 0.4]
# q_losses = [-2]

# ************************************************************************************ lq_loss
# # we are not applying mixup, so:
# mixup_warmup_epochs = [-1]
# mixup_alphas = [-1]
# losses = ['lq_loss']
# q_losses = [0.2, 0.4, 0.5, 0.6, 0.8]
# output_file = 'crnn_seld_Q_explore_net_tagger_BETA_lq_loss'





losses = ['CCE']  # CCE_diy_max, lq_loss, CCE_diy_outlier, CCE, CCE_diy_max_origin, CCE_diy_outlier_origin, lq_loss_origin
# losses = ['lq_loss']  # CCE_diy_max, lq_loss, CCE_diy_outlier, CCE, CCE_diy_max_origin, CCE_diy_outlier_origin, lq_loss_origin
# q_losses = [0.3, 0.5, 0.7]

# vip define the path of the yaml with (most) of the parameters that define the experiment
yaml_file = 'params_edu_v1_final_submission.yaml'


def change_yaml(fname, count_trial, output_file, model, loss, patch_len, lr, batch_size, cnn_nb_filt, rnn_nb, fc_nb, n_mel, mixup_warmup_epoch, mixup_alpha):
    """
    Modifies the yaml fiven by fname according to the input parameters.
    This allows to test several values for hyper-parameter(s) on the same run
    :param fname:
    :param count_trial:
    :param train_data:
    :param output_file:
    :param model:
    :param loss:
    :param q_loss:
    :return:
    """

    stream = open(fname, 'r')
    data = yaml.load(stream)

    data['ctrl']['count_trial'] = count_trial
    data['ctrl']['output_file'] = output_file
    data['learn']['model'] = model
    data['loss']['type'] = loss

    # watch basic
    data['learn']['lr'] = lr
    data['learn']['batch_size'] = batch_size
    data['extract']['patch_len'] = patch_len
    data['extract']['mode_last_patch'] = mode_last_patch
    data['extract']['n_mels'] = n_mel

    # watch CRNN
    data['crnn']['cnn_nb_filt'] = cnn_nb_filt
    data['crnn']['rnn_nb'] = rnn_nb
    data['crnn']['fc_nb'] = fc_nb
    data['crnn']['dropout_rate'] = dropout_rate


    # watch LSR
    data['learn']['LSR'] = False
    data['learn']['LSRmode'] = False    # GROUPS2 GROUPS3 WEIGHTS_CC WEIGHTS_CC+
    data['learn']['eps_LSR_noisy'] = False       # False, epsi
    data['learn']['distri_prior_LSR'] = False    # False=uniform, 'noise', 'unigram'
    data['learn']['delta_k_LSR'] = 38            # 2,4,6,8, only for noise distri

    data['learn']['delta_eps_LSR'] = False      # this is concurrent to all distris. put to False if undesired
    data['learn']['LSRmapping'] = False         # LSRmapping False

    # watch 2 stage learning***********************, just define the minimum to ignore
    data['learn']['stages'] = 1                  #usually 1 or 2. but 0 for enabling mixup_warmup

    # watch 1 stage dropout***********************
    data['learn']['dropout'] = False                    # True False
    data['learn']['dropout_prob'] = False       # only used if True

    # watch 1 stage mixup***********************, if I dont wanna use it
    # data['learn']['mixup'] = False                    # True False
    # data['learn']['mixup_mode'] = False
    # data['learn']['mixup_alpha'] = False
    # data['learn']['mixup_log'] = False
    # data['learn']['mixup_clamp'] = False
    # data['learn']['mixup_warmup_epochs'] = False

    # watch 1 stage mixup*********************** this is the good one
    # data['learn']['stages'] = enable_mixup_warmup  #for enabling mixup_warmup
    data['learn']['stages'] = 1                  #usually 1 or 2. but 0 for enabling mixup_warmup
    data['learn']['mixup'] = True                    # True False
    data['learn']['mixup_mode'] = mixup_mode
    data['learn']['mixup_alpha'] = mixup_alpha
    data['learn']['mixup_log'] = mixup_log
    data['learn']['mixup_clamp'] = mixup_clamp
    data['learn']['mixup_warmup_epochs'] = mixup_warmup_epoch

    # watch lqloss***********************
    # data['loss']['q_loss'] = q_loss

    data['learn']['early_stop'] = 'val_acc'        # True False

    with open(fname, 'w') as yaml_file:
        yaml_file.write(yaml.dump(data, default_flow_style=False))


def main():

    # to append suffix and store some results for every trial of the experiment (usually 6 trials)
    count_trial = 0

    for kk in np.arange(N):
        # consistency
        for model in models:
            for loss in losses:
                for lr in lrs:
                    for patch_len in patch_lens:
                        for batch_size in batch_sizes:
                            for cnn_nb_filt in cnn_nb_filts:
                                for rnn_nb in rnn_nbs:
                                    for fc_nb in fc_nbs:
                                        for n_mel in n_mels:
                                            for mixup_warmup_epoch in mixup_warmup_epochs:
                                                for mixup_alpha in mixup_alphas:
                                                    # for q_loss in q_losses:

                                                    count_trial += 1

                                                    change_yaml(yaml_file,
                                                                count_trial=count_trial,
                                                                output_file=output_file,
                                                                model=model,
                                                                loss=loss,
                                                                patch_len=patch_len,
                                                                lr=lr,
                                                                batch_size=batch_size,
                                                                cnn_nb_filt=cnn_nb_filt,
                                                                rnn_nb=rnn_nb,
                                                                fc_nb=fc_nb,
                                                                n_mel=n_mel,
                                                                mixup_warmup_epoch=mixup_warmup_epoch,
                                                                mixup_alpha=mixup_alpha,
                                                                )

                                                    # call the job
                                                    str_exec = 'python classify_submission_eval.py -p ' + yaml_file
                                                    print(str_exec)
                                                    # CUDA_VISIBLE_DEVICES=0 KERAS_BACKEND=tensorflow python jobPlan.py &> logs/pro4_model_set_approach_hyper.out

                                                    try:
                                                        retcode = subprocess.call(str_exec, shell=True)
                                                        if retcode < 0:
                                                            print("Child was terminated by signal", -retcode, file=sys.stderr)
                                                        else:
                                                            print("Child returned", retcode, file=sys.stderr)
                                                    except OSError as e:
                                                        print("Execution failed:", e, file=sys.stderr)

    end = time.time()

    str_result_generate = "sed -n -e 's/^.*Mean Accuracy for files evaluated: //p' logs/" + output_file + ".out | tr '\n' ',' > logs/" + output_file + ".csv"

    retcode_res = subprocess.call(str_result_generate, shell=True)
    if retcode_res < 0:
        print("Child was terminated by signal", -retcode_res, file=sys.stderr)
    else:
        print("Child returned", retcode_res, file=sys.stderr)

    #
    print('\n=============================List of jobs finalized=================================================\n')
    print('\nTime elapsed for the LIST of jobs: %7.2f hours' % ((end - start) / 3600.0))
    print('\n====================================================================================================\n')

    return 0


if __name__ == '__main__':
    main()