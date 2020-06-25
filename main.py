import random

# グラフ描写用
import matplotlib.pyplot as plt
import japanize_matplotlib

# 定数
WEIGHT_LIMIT = 5000
POPULATION = 10
MAX_GENERATION = 100

# グラフ描画用
average_fitness = []
max_fitness = []
generations = []

# 各個体の適応度の計算用
def get_elements_gene_weight_and_value(elements_gene, elements_number, elements_weight, elements_value):
  elements_gene_weight = []
  elements_gene_value = []
  for i in range(0, POPULATION):
    elements_gene_weight.append(0)
    elements_gene_value.append(0)   
    for j in range(0, elements_number):
      # 適応度関数の処理
      if elements_gene[i][j]:
        elements_gene_weight[i] += elements_weight[j]
        elements_gene_value[i] += elements_value[j]
      if elements_gene_weight[i] > WEIGHT_LIMIT:
        elements_gene_value[i] = 0
  return [elements_gene_weight, elements_gene_value]

# デバッグ出力用
def print_params(elements_gene_weight, elements_gene_value, elements_gene, now_generation, elements_weight, elements_value, elements_value_and_weight):
  if now_generation == 1:
    print("質量 :", elements_weight)
    print("質量最大値 :", WEIGHT_LIMIT)
    print("適応度 :", elements_value)
    print()

  print("総質量 :", elements_gene_weight)
  print("総適応度(世代{}) : {}".format(now_generation, elements_gene_value))
  print("平均適応度:", sum(elements_gene_value) / len(elements_gene_value))
  print("最大適応度:", max(elements_gene_value))
  average_fitness.append(sum(elements_gene_value) / len(elements_gene_value))
  max_fitness.append(max(elements_gene_value))
  for x_num, select_list in enumerate(elements_gene):
    print("個体{}の選択元素:".format(x_num + 1), end='')
    for i, is_select in enumerate(select_list):
      if is_select:
        print(list(elements_value_and_weight.keys())[i], end=" ")
    print()
  print()


# エリートの保存用
def get_elite_gene(elements_gene, elements_gene_value):
  sorted_index_list = sorted(range(len(elements_gene_value)),
    key=lambda k: elements_gene_value[k], reverse=True)
  return [
    elements_gene[sorted_index_list[0]]
  ]

# エリート以外の選択, ルーレット選択用
def get_except_elite_gene(elements_gene_value, elements_gene, elements_number):
  except_elite_gene = []

  for i in range(0, POPULATION):
    except_elite_gene.append([0] * elements_number)

  total = sum(elements_gene_value)
  for x in range(0, POPULATION):
    break_condition = int(random.random() * total)
    total = sum(elements_gene_value)
    for i in range(0, POPULATION):
      if total > break_condition:
        for j in range(0, elements_number):
          except_elite_gene[x][j] = elements_gene[i][j]
        break
  return except_elite_gene

# 2点交叉用
def two_point_crossover(except_elite_gene, elements_number):
  loop_counter = 0
  while (POPULATION % 2 == 1 and loop_counter < POPULATION -1) or (POPULATION % 2 == 0 and loop_counter < POPULATION):
    crossrate = 0.9
    if random.random() <= crossrate:
      first_cross_index = int(random.random() * elements_number)
      second_cross_index = first_cross_index + int(
        random.random() * (elements_number - first_cross_index)
      )
      child = [[0]*elements_number, [0]*elements_number]

      for i in range(0, elements_number):
        child_first_index = first_cross_index <= i and i <= second_cross_index
        child[child_first_index][i] = except_elite_gene[loop_counter][i]
        child[not child_first_index][i] = except_elite_gene[loop_counter+1][i]
        except_elite_gene[loop_counter][i] = child[0][i]
        except_elite_gene[loop_counter+1][i] = child[1][i]
    loop_counter += 2
  return except_elite_gene

# 突然変異用
def mutate(except_elite_gene, elements_number):
  for i in range(0, POPULATION):
    mutate_rate = 0.05 # 突然変異率
    if random.random() <= mutate_rate:
      gene_index = int(random.random()*elements_number)
      except_elite_gene[i][gene_index] = (except_elite_gene[i][gene_index] + 1) % 2
  return except_elite_gene

# 世代の更新用
def update_generation(elements_gene, elite_gene, except_elite_gene, elements_number):
  for i in range(0, POPULATION):
    for j in range(0, elements_number):
      if i == 0 and elite_gene != None:
        elements_gene[i][j] = elite_gene[i][j]
      else:
        elements_gene[i][j] = except_elite_gene[i][j]
  return elements_gene

# メイン処理
def main():
  elements_weight = []
  elements_value = []

  # 元素名: [価値, 容量(g)]
  elements_value_and_weight = {
    '金': [6700, 10],
    '銀': [63, 100],
    '銅': [0.85, 1000],
    'プラチナ': [3100,10],
    'リチウム': [0.58, 1000],
    'ベリリウム': [4.5, 100],
    'ホウ素': [550, 10],
    'チタン': [1.3, 1000],
    'バナジウム': [4.3, 1000],
    'クロム': [0.28, 1000],
    'マンガン': [0.19, 1000],
    'コバルト': [6.6, 100],
    'ニッケル': [3.2, 10],
    'ガリウム': [140, 10],
    'ゲルマニウム': [87, 1000],
    'セレン': [8.8, 1000],
    'ルビジウム': [2400, 100],
    'ストロンチウム': [7.4, 10],
    'ジルコニウム': [0.09, 1000],
    'ニオブ': [8, 10]
  }
  elements_number = len(elements_value_and_weight.keys())

  for element_name in elements_value_and_weight:
    elements_value.append(elements_value_and_weight[element_name][0])
    elements_weight.append(elements_value_and_weight[element_name][1])

  elements_gene = []
  for _ in range(0, POPULATION):
    temp = []
    for _ in range(0, elements_number):
      temp.append(int(random.random()*2))
    elements_gene.append(temp)

  # ここまでが初期生物集団の発生処理

  # ここで世代が一定まで到達し終了するか,もしくは 処理の継続するかの判定
  for now_generation in range(1, MAX_GENERATION + 1):

    # 各個体の適応度の計算
    elements_gene_weight, elements_gene_value = get_elements_gene_weight_and_value(elements_gene, elements_number, elements_weight, elements_value)

    # 淘汰及び増殖の実行
    # エリートの選択
    elite_gene = get_elite_gene(elements_gene, elements_gene_value) # エリート保存なしの場合はここを None に変更する
    # エリート以外の選択, ルーレット選択
    except_elite_gene = get_except_elite_gene(elements_gene_value, elements_gene, elements_number)

    # 遺伝子型の交叉の実行
    except_elite_gene = two_point_crossover(except_elite_gene, elements_number)

    # 突然変異の実行
    except_elite_gene = mutate(except_elite_gene, elements_number)

    # 世代の更新, エリートの反映
    elements_gene = update_generation(elements_gene, elite_gene, except_elite_gene, elements_number)

    # デバッグ出力
    print_params(elements_gene_weight, elements_gene_value, elements_gene, now_generation, elements_weight, elements_value, elements_value_and_weight)
    generations.append(now_generation)

if __name__ == '__main__':
  # メイン処理
  main()

  # 以下グラフ出力処理
  fig = plt.figure()
  ax = fig.add_subplot()
  ax.plot(generations, average_fitness, marker='', label='average_fitness')

  plt.title('世代と平均適応度の関係')
  plt.xlabel('世代(1〜{})'.format(MAX_GENERATION))
  plt.ylabel('平均適応度')

  plt.show()
  fig = plt.figure()
  ax = fig.add_subplot()
  ax.plot(generations, max_fitness, marker='', label='max_fitness')
  plt.title('世代と最大適応度の関係')
  plt.xlabel('世代(1〜{})'.format(MAX_GENERATION))
  plt.ylabel('最大適応度')
  plt.show()
