import math
from sklearn.feature_extraction.text import CountVectorizer
from lda import LDA
import math
import matplotlib.pyplot as plt



class TopicModelingMetrics(object):
	"""docstring for TopicModelingMetrics"""
	def __init__(self):
		super(TopicModelingMetrics, self).__init__()
	
	def calculate(self,topic_words,topic_k,word_v):
		pass

class TopicSimpleScore(TopicModelingMetrics):
	"""
	Probablidad de que word_v pertenezca al topico topic_k
	"""

	def __init__(self):
		super(TopicSimpleScore, self).__init__()

	def calculate(self,topic_words,topic_k,word_v):
		return topic_words[topic_k][word_v]


class TopicTermScore(TopicModelingMetrics):
	"""
	Score propuesto por Blei y Lafferty en Topic Models. In Text Mining: Theory and Applications
	Resalta palabras con una alta probablidad de ocurrencia en un topico y baja probabilidad en el resto de topicos
	"""
	
	def __init__(self):
		super(TopicTermScore, self).__init__()

	def get_tf_topic(self,topic_words,topic_k,word_v):
		return topic_words[topic_k][word_v]

	def get_idf_topic(self,topic_words,topic_k,word_v):
		num_topics = topic_words.shape[0]
		bkn = topic_words[topic_k][word_v]
		value = 1.0
		for topic_dist in topic_words:
			value = value*topic_dist[word_v]
		return math.log(1.0*bkn/math.pow(value,1.0/num_topics))
	
	def calculate(self,topic_words,topic_k,word_v):
		tf_topic = self.get_idf_topic(topic_words,topic_k,word_v)
		idf_topic = self.get_idf_topic(topic_words,topic_k,word_v)
		return tf_topic*idf_topic

class TopicModelingLDA(object):
	#wrapper de la libreriar LDA
	#permite caracterizar los topicos en base a varios scores encontrados en la literatura

	def __init__(self,corpus,metrics_criteria='simple'):
		super(TopicModelingLDA, self).__init__()
		self.corpus = corpus
		self.select_metric_criteria(metrics_criteria)
		self.model = None
		self.topic_words = None
		self.top_words = None
		self.all_words = []

	def fit(self,num_topic=5,n_iter=1500):
		count_vect = CountVectorizer()
		x_train_counts = count_vect.fit_transform(self.corpus)
		self.model = LDA(n_topics=num_topic, n_iter=n_iter, random_state=1)
		self.model.fit(x_train_counts)

		self.topic_words = self.model.topic_word_
		self.vocabulary = count_vect.get_feature_names()

	def select_metric_criteria(self,metrics_criteria):
		if metrics_criteria == 'term_score':
			self.metrics = TopicTermScore()
		else:
			self.metrics = TopicSimpleScore()

	def get_highest_scores(self,k_top=10):
		#topic_words es una matriz (numero de topicos,palabras)
		#la fila k indica la distribucion de palabras del topico k
		num_topics = len(self.topic_words) 
		print ("Numero de topicos",num_topics)
		top_words = []
		self.top_words = {}

		for topic_k in range(num_topics):
			scores = []
			for v,word in enumerate(self.vocabulary):
				score = self.metrics.calculate(self.topic_words,topic_k,v)
				scores.append((word,score))
			scores.sort(key=lambda tup: tup[1]) 
			scores = scores[-k_top:]
			
			print ("Topico %d"%(topic_k))
			for word,score in scores:
				print ("%s,%.4f"%(word,score))
			print ("")

			self.top_words[topic_k] = [{'word':word,'score':score} for word,score in scores]
			self.all_words += [ word for word,score in scores]

		return self.top_words

	def get_all_words(self):
		return self.all_words

class TopicModelingEvaluator(object):
	"""docstring for TopicModelingEvaluator"""
	def __init__(self,corpus,num_topics = [5,10,20]):
		#calcula perplexity para cada valor del arregloe num topics
		#llame a show_perplexity para observar la distribucion de perplexity sobre el numero de topicos
		super(TopicModelingEvaluator, self).__init__()
		self.num_topics = num_topics
		self.corpus = corpus
	
	def show_perplexity(self):
		perplexity  = [self.calculate_perplexity(num_topic) for num_topic in self.num_topics]
		plt.plot(self.num_topics,perplexity)
		plt.xlabel("Num topics")
		plt.ylabel("Perplexity")
		plt.show()

	def calculate_perplexity(self,num_topic):
		lda_wrapper = TopicModelingLDA(self.corpus)
		lda_wrapper.fit(num_topic,10)

		log_likelihood = lda_wrapper.model.loglikelihood()
		n_features = lda_wrapper.topic_words.shape[1]
		x = 1.0*log_likelihood/n_features
		result = math.exp(-1.0*x)
		return result