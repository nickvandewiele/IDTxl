import get_realisations
import numpy as np

def nonuniform_embedding(data, idx_current_value, idx_candidate_set, conditional = np.array([])):

    significant = True
    max_mi = -float("inf")
    idx_max_mi = np.nan
    realisations_current_value = get_realisations.single_process(data, idx_current_value)

    for process in data.size[0]:
        for idx_sample in idx_candidate_set:
            realisations_current_candidate = get_realisations.single_process(data[process], idx_sample)
            temp_mi = mi_calculator_kraskov(realisations_current_value, realisations_current_candidate)
            if temp_mi > max_mi:
                max_mi = temp_mi
                idx_max_mi = idx_sample
    conditional.append(idx_max_mi)

    while significant:
        for process in data.size[0]:
            for idx_sample in idx_candidate_set:
                realisations_current_candidate = get_realisations.single_process(data[process], idx_sample)
                temp_cmi = cmi_calculator_kraskov(realisations_current_value, realisations_current_candidate)
                if temp_cmi > max_cmi:
                    max_cmi = temp_cmi
                    idx_max_cmi = np.array([process, idx_sample])
        significant = maximum_statistic(data, conditional, max_cmi)
        conditional.append(idx_max_cmi)

    conditional.pop() # if the while loop is left the last addition wasn't significant and needs to be removed

    return conditional
