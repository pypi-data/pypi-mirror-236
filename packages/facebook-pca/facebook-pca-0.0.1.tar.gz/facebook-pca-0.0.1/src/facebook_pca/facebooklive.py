#라이브러리 import
def set_libraries():
  import pandas as pd
  import seaborn as sns
  import matplotlib.pyplot as plt
  from sklearn.decomposition import PCA
  from sklearn.cluster import KMeans
  import seaborn as sns
  from matplotlib import pyplot as pl
  import numpy as np
  import matplotlib.pyplot as plt
  import matplotlib.cm as cm
  from sklearn.preprocessing import StandardScaler
  from sklearn.cluster import KMeans, DBSCAN
  from sklearn.decomposition import PCA
  from sklearn import metrics
  import warnings
  warnings.filterwarnings('ignore')
    
#데이터 확인
def data_check(data):
  print("data shape: ",data.shape)
  print("<결측치>")
  print(data.isnull().sum())
  data.head()
    
#데이터 전처리
def data_preprocessing(data):
  features = list(data.columns)[:-4]
  df = data[features]
  print("결측치 column drop 완료")

  df = df.drop('status_published', axis=1)
  df = df.drop('status_id', axis=1)
  print("id, published column drop 완료")

  from sklearn import preprocessing
  label_encoder = preprocessing.LabelEncoder()
  df['status_type'] = label_encoder.fit_transform(df['status_type'])
  print("범주형 column labeling 완료")

  df.head()

  return df

#PCA component 출력
def pca_components(df):
  from sklearn.decomposition import PCA
  import matplotlib.pyplot as plt
  import numpy as np

  pca = PCA(svd_solver='randomized', random_state=123)
  pca.fit(df)
  print("PCA model fitting...")

  fig = plt.figure(figsize=(10,5))
  plt.plot(np.cumsum(pca.explained_variance_ratio_))
  plt.xlabel('number of components')
  plt.ylabel('cumulative explained variance')
  plt.show()

  print("PCA explained variance ratio: ",pca.explained_variance_ratio_[0:2].sum().round(3),
  pca.explained_variance_ratio_[0:3].sum().round(3),
  pca.explained_variance_ratio_[0:4].sum().round(3))

  print("1st component_explained variance ratio: ",pca.explained_variance_ratio_[0])
  print("2nd component_explained variance ratio: ",pca.explained_variance_ratio_[1])
    
#k-means cluster 개수
def cluster_num(df):
  import matplotlib.pyplot as plt
  from sklearn.cluster import KMeans
  
  wss = []
  K = range(2,11)
  for k in K:
      kmeans = KMeans(n_clusters=k, random_state=123)
      kmeans = kmeans.fit(df)
      wss.append(kmeans.inertia_)
  plt.plot(K, wss, "k*-")
  plt.xlabel("Number of clusters k")
  plt.ylabel("Total Within Sum of Squares")
  plt.title("Optimal number of clusters")
  plt.show()

#PCA 시각화
def plot_PCA(df):
  from sklearn.decomposition import PCA
  import matplotlib.pyplot as plt
  from sklearn.cluster import KMeans
  import pandas as pd

  pca = PCA()
  pca_data = pca.fit_transform(df)
  pca_data = pd.DataFrame(pca_data, columns=["pc"+str(i+1) for i in range(len(df.columns))])

  pca_data1 = pca_data[["pc1","pc2"]].copy()
  data1 = df.copy()

  kmeans = KMeans(n_clusters=2, random_state=2464063)
  data1["clusters"] = kmeans.fit_predict(data1)

  plt.scatter(pca_data1["pc1"], pca_data1["pc2"], c=data1.clusters)
  plt.title("The visualization of the clustered data")
  plt.xlabel("pc1:" + "{:.2f}".format(pca.explained_variance_ratio_[0] * 100) + " %")
  plt.ylabel("pc2:" + "{:.2f}".format(pca.explained_variance_ratio_[1] * 100) + " %")
  plt.show()
    
 #실루엣 score
def silhouette_score(df):
  from sklearn.cluster import KMeans
  from sklearn import metrics

  range_n_clusters = list(range(2,10))
  for n_clusters in range_n_clusters:
    clusterer = KMeans(n_clusters=n_clusters)
    preds = clusterer.fit_predict(df)
    centers = clusterer.cluster_centers_

    Kmeans_score = metrics.silhouette_score(df, preds)
    print("For n_clusters = {}, silhouette score is {})".format(n_clusters, Kmeans_score))