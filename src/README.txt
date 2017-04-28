-------------------------------------------------------------------
---------------------------源码说明--------------------------------
-------------------------------------------------------------------
- 运行环境说明
-------------------------------------------------------------------
- 首先由基本的深度学习运行环境
- 安装theano
- 导入Lasagne库
-------------------------------------------------------------------
- 源码使用说明（只对每个目录下用于执行的代码用法进行说明）
-------------------------------------------------------------------
- data_prepare
	- 该目录下的代码用于完成对图片的裁剪复制以及向量化
	- *_img_crop.py
		- 用来裁剪复制图片
		- Usage: python *_img_crop.py aligned_db_folder new_folder
			- aligned_db_folder: 原始文件夹
			- new_folder: 结果文件夹，与原始文件夹的文件夹结构一样
	- *_data_split.py
		- 用来切分数据，将数据分为训练集和验证集
		- Usage: python youtube_data_split.py src_folder test_set_file train_set_file
			- src_folder: 原始文件夹，此处应该为img_crop.py处理所得的新文件夹
			- test_set_file: 验证集图片路径集合文件
			- train_set_file: 训练集图片路径集合文件
	- vectorize_img.py
		- 用来将图像向量化，每张图像都是47×55的，所以每张图片变成一个47×55×3的向量
		- Usage: python vectorize_img.py test_set_file train_set_file test_vector_folder train_vector_folder
			- test_set_file: *_data_split.py生成的
			- train_set_file: *_ata_split.py生成的
			- test_vector_folder: 存储验证集向量文件的文件夹名称
			- train_vector_folder: 存储训练集向量文件的文件夹名称
	- lfw_data_split_bypairs.py
		- 用来将LFW数据集按照pairs.txt分为6000对验证用例，用于后续naive_verify
		- Usage: python lfw_data_split_bypairs.py src_folder pairs_file left_set_file right_set_file
			- src_folder: 原始文件夹，此处应该为img_crop.py处理所得的新文件夹
			- pairs_file: pairs.txt，存放6000对匹配
			- left_set_file：6000对样例第一张人脸向量存放路径
			- right_set_file：6000对样例第二张人脸向量存放路径
-------------------------------------------------------------------
- conv_net
	- 该目录下的代码用于训练和验证（人脸识别）DeepID网络
	- deepid_class.py
		- Usage: python deepid_class.py vec_valid vec_train params_file
			- vec_valid: vectorize_img.py生成的
			- vec_train: vectorize_img.py生成的
			- params_file: 用来存储训练时每次迭代的参数，以及后续使用参数抽取特征
	- deepid_generate.py
		- 抽取DeepID的隐含层，即160-d的那一层
		- Usage: python deepid_generate.py dataset_folder params_file result_folder
			- dataset_folder: 可以是训练集向量文件夹或者验证集向量文件夹
			- params_file: deepid_class.py训练得到
			- result_folder: 结果文件夹，其下的文件与dataset_folder中文件的文件名一一对应，但是结果文件夹中的向量的长度变为160而不是原来的7755
-------------------------------------------------------------------
- verify_naive
	- 该目录下的代码用于完成简单的相似性度量方法，包括欧几里得距离和余弦相似性
	- verify.py
		- Usage: python verify.py exp_param result_file
			- exp_param: 配置文件
				- 样例配置文件如下：
				
				test_data_folder: left_vec
				train_data_folder: right_vec
				# this should be in the same folder with left_vec and right_vec
				# and the program should be executed in the same folder with this file

				[exp_1]
				description: verify based on pca dimension reduction to 160 with Euclidean
				pre_process_method: pca
				sim_metric_method: euc
				components: 160

				[exp_2]
				description: verify based on pca dimension reduction to 160 with cosine
				pre_process_method: pca
				sim_metric_method: cos
				components: 160
				
				前5行定义基本信息
				- line 1：查询集向量文件夹
				- line 2：被查询集向量文件夹
				- line 3/4：注释内容
				- line 5：空行

				再下面定义每个实验的实验参数，以exp_6为例：
				- line 1: 实验id，可以随意命名，必不可少
				- line 2: 实验描述，对实验总体描述，必不可少
				- line 3: 预处理方法，目前只有pca和None两种，必不可少
				- line 4: 距离度量方法，目前只有cos和euc两种，必不可少
			- result_file：存储验证结果，用于作图
-------------------------------------------------------------------
- joint_bayesian
	- 该目录下的代码用于完成JointBayesian模型的训练和验证
	- lfw_to_mat.py
		- 用于将LFW预处理后形成的图片处理为mat格式并保存，并根据pairs.txt生成对应的pairlist.mat文件
		- Usage: python lfw_to_mat.py src_folder pairslist result_folder
			- src_folder：原始文件夹，此处应该为img_crop.py处理所得的新文件夹
			- pairslist：pairs.txt，存放6000对匹配 
			- result_folder：存放生成mat文件的目录
	- deepid_to_mat.py
		- 用于将LFW经过网络提取所得的DeepID pkl文件转换为mat文件作为JointBayesian模型的输入
		- Usage: python deepid_to_mat.py dataset_folder result_folder
			- dataset_folder：存放DeepID pkl文件的目录
			- result_folder：存放生成mat文件的目录
	- verify_lfw_pca.py
		- 用于训练JointBayesian模型，并验证PCA降维特征的人脸认证效果
		- 注意查看代码设置好读取数据的路径
	- verify_lfw_deepid.py
		- 用于验证deepid_to_mat.py提取得到的DeepID的人脸认证效果
		- 注意查看代码设置好读取数据的路径
-------------------------------------------------------------------
- visualization
	- 该目录下的代码用于将前述代码生成的一些数据文件进行图形化显示，目录下也放有相应数据
	- 查看代码确认相应plot.py对应的数据文件即可
	- 对应关系如下：
		- plot.py：webface-5.25.txt(DeepID训练和验证数据)
		- plot_csv_all.py：*.csv(naive_verify的验证结果)
		- plot_jointBayes.py：draw_file_*.txt(JointBayesian的验证结果)
-------------------------------------------------------------------