-------------------------------------------------------------------
---------------------------Դ��˵��--------------------------------
-------------------------------------------------------------------
- ���л���˵��
-------------------------------------------------------------------
- �����ɻ��������ѧϰ���л���
- ��װtheano
- ����Lasagne��
-------------------------------------------------------------------
- Դ��ʹ��˵����ֻ��ÿ��Ŀ¼������ִ�еĴ����÷�����˵����
-------------------------------------------------------------------
- data_prepare
	- ��Ŀ¼�µĴ���������ɶ�ͼƬ�Ĳü������Լ�������
	- *_img_crop.py
		- �����ü�����ͼƬ
		- Usage: python *_img_crop.py aligned_db_folder new_folder
			- aligned_db_folder: ԭʼ�ļ���
			- new_folder: ����ļ��У���ԭʼ�ļ��е��ļ��нṹһ��
	- *_data_split.py
		- �����з����ݣ������ݷ�Ϊѵ��������֤��
		- Usage: python youtube_data_split.py src_folder test_set_file train_set_file
			- src_folder: ԭʼ�ļ��У��˴�Ӧ��Ϊimg_crop.py�������õ����ļ���
			- test_set_file: ��֤��ͼƬ·�������ļ�
			- train_set_file: ѵ����ͼƬ·�������ļ�
	- vectorize_img.py
		- ������ͼ����������ÿ��ͼ����47��55�ģ�����ÿ��ͼƬ���һ��47��55��3������
		- Usage: python vectorize_img.py test_set_file train_set_file test_vector_folder train_vector_folder
			- test_set_file: *_data_split.py���ɵ�
			- train_set_file: *_ata_split.py���ɵ�
			- test_vector_folder: �洢��֤�������ļ����ļ�������
			- train_vector_folder: �洢ѵ���������ļ����ļ�������
	- lfw_data_split_bypairs.py
		- ������LFW���ݼ�����pairs.txt��Ϊ6000����֤���������ں���naive_verify
		- Usage: python lfw_data_split_bypairs.py src_folder pairs_file left_set_file right_set_file
			- src_folder: ԭʼ�ļ��У��˴�Ӧ��Ϊimg_crop.py�������õ����ļ���
			- pairs_file: pairs.txt�����6000��ƥ��
			- left_set_file��6000��������һ�������������·��
			- right_set_file��6000�������ڶ��������������·��
-------------------------------------------------------------------
- conv_net
	- ��Ŀ¼�µĴ�������ѵ������֤������ʶ��DeepID����
	- deepid_class.py
		- Usage: python deepid_class.py vec_valid vec_train params_file
			- vec_valid: vectorize_img.py���ɵ�
			- vec_train: vectorize_img.py���ɵ�
			- params_file: �����洢ѵ��ʱÿ�ε����Ĳ������Լ�����ʹ�ò�����ȡ����
	- deepid_generate.py
		- ��ȡDeepID�������㣬��160-d����һ��
		- Usage: python deepid_generate.py dataset_folder params_file result_folder
			- dataset_folder: ������ѵ���������ļ��л�����֤�������ļ���
			- params_file: deepid_class.pyѵ���õ�
			- result_folder: ����ļ��У����µ��ļ���dataset_folder���ļ����ļ���һһ��Ӧ�����ǽ���ļ����е������ĳ��ȱ�Ϊ160������ԭ����7755
-------------------------------------------------------------------
- verify_naive
	- ��Ŀ¼�µĴ���������ɼ򵥵������Զ�������������ŷ����þ��������������
	- verify.py
		- Usage: python verify.py exp_param result_file
			- exp_param: �����ļ�
				- ���������ļ����£�
				
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
				
				ǰ5�ж��������Ϣ
				- line 1����ѯ�������ļ���
				- line 2������ѯ�������ļ���
				- line 3/4��ע������
				- line 5������

				�����涨��ÿ��ʵ���ʵ���������exp_6Ϊ����
				- line 1: ʵ��id�����������������ز�����
				- line 2: ʵ����������ʵ�������������ز�����
				- line 3: Ԥ��������Ŀǰֻ��pca��None���֣��ز�����
				- line 4: �������������Ŀǰֻ��cos��euc���֣��ز�����
			- result_file���洢��֤�����������ͼ
-------------------------------------------------------------------
- joint_bayesian
	- ��Ŀ¼�µĴ����������JointBayesianģ�͵�ѵ������֤
	- lfw_to_mat.py
		- ���ڽ�LFWԤ������γɵ�ͼƬ����Ϊmat��ʽ�����棬������pairs.txt���ɶ�Ӧ��pairlist.mat�ļ�
		- Usage: python lfw_to_mat.py src_folder pairslist result_folder
			- src_folder��ԭʼ�ļ��У��˴�Ӧ��Ϊimg_crop.py�������õ����ļ���
			- pairslist��pairs.txt�����6000��ƥ�� 
			- result_folder���������mat�ļ���Ŀ¼
	- deepid_to_mat.py
		- ���ڽ�LFW����������ȡ���õ�DeepID pkl�ļ�ת��Ϊmat�ļ���ΪJointBayesianģ�͵�����
		- Usage: python deepid_to_mat.py dataset_folder result_folder
			- dataset_folder�����DeepID pkl�ļ���Ŀ¼
			- result_folder���������mat�ļ���Ŀ¼
	- verify_lfw_pca.py
		- ����ѵ��JointBayesianģ�ͣ�����֤PCA��ά������������֤Ч��
		- ע��鿴�������úö�ȡ���ݵ�·��
	- verify_lfw_deepid.py
		- ������֤deepid_to_mat.py��ȡ�õ���DeepID��������֤Ч��
		- ע��鿴�������úö�ȡ���ݵ�·��
-------------------------------------------------------------------
- visualization
	- ��Ŀ¼�µĴ������ڽ�ǰ���������ɵ�һЩ�����ļ�����ͼ�λ���ʾ��Ŀ¼��Ҳ������Ӧ����
	- �鿴����ȷ����Ӧplot.py��Ӧ�������ļ�����
	- ��Ӧ��ϵ���£�
		- plot.py��webface-5.25.txt(DeepIDѵ������֤����)
		- plot_csv_all.py��*.csv(naive_verify����֤���)
		- plot_jointBayes.py��draw_file_*.txt(JointBayesian����֤���)
-------------------------------------------------------------------