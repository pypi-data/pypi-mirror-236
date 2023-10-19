from pyoptquest import OptQuestOptimizer

prod_time = [7, 13, 2, 4, 21, 6, 8, 12, 17, 22]
trans_mat = [[-1, 9, 13, 6, 7, 8, 3, 17, 7, 3],
             [3, -1, 8, 7, 9, 4, 3, 16, 3, 8],
             [5, 0, -1, 8, 7, 9, 4, 3, 16, 5],
             [7, 2, 5, -1, 4, 2, 5, 7, 2, 5],
             [4, 3, 4, 7, -1, 4, 3, 4, 7, 3],
             [2, 14, 7, 7, 5, -1, 1, 4, 6, 4],
             [8, 7, 9, 4, 16, 3, -1, 4, 9, 7],
             [11, 5, 2, 3, 2, 6, 4, -1, 9, 7],
             [4, 2, 12, 9, 1, 5, 5, 6, -1, 9],
             [9, 3, 6, 7, 8, 3, 17, 7, 3, -1]]


def cost_evaluator(inputs):
    perm_group = inputs['products']
    prod_cost = sum([prod_time[int(i) - 1] for i in perm_group])
    trans_cost = 0
    for i in range(len(perm_group) - 1):
        idx1 = int(perm_group[i]) - 1
        idx2 = int(perm_group[i + 1]) - 1
        trans_cost += trans_mat[idx1][idx2]

        # return results
        outputs = {'cost': prod_cost + trans_cost}
        return outputs


# define input(s)
search_space = {
    'products': {'type': 'permutation', 'elements': ['prod_A', 'prod_B', 'prod_C', 'prod_D', 'prod_E', 'prod_F']}#, 'prod_g', 'prod_h', 'prod_i', 'prod_j']}
    # , 'prod_G', 'prod_H', 'prod_I', 'prod_J']},
}

# define output(s)
output_space = [
    'cost'
]

# define objective(s)
objectives = {
    'obj': {'type': 'min', 'expression': 'cost'}
}

# define the optimization
opt = OptQuestOptimizer(
    search_space=search_space,
    objectives=objectives,
    evaluator=cost_evaluator,
    output_space=output_space,
    license_id=999999999,
    optquest_jar=r'../OptQuest.jar')
opt.search(n_iter=20)

# print results
print('best score:', opt.best_score)
print('best parameters:', opt.best_para)
print('Optimization time:', opt.optimization_time)
