class Pracklr:
    def avail_prog():
        avail_lx = r"""
        ___Hadoop HDFS__
        
        2.  MAKING AND LISTING DIRECTORIES

	cd $HADOOP_HOME
	start-all.sh
	jps
	hdfs dfs -mkdir /DD
	hdfs dfs -ls /

	3.  A EXPORTING DATA IN HADOOP AND CHANGING FILE/FOLDER PERMISSION

	touch sampleda.txt
	hdfs dfs -put sampleda.txt /DD
	hdfs dfs -chmod 777 /DD/sampleda.txt
	hdfs dfs -get /DD/sampleda.txt
	hdfs dfs -ls /

	4.  PRINTING,DISPLAYING THE SIZE AND DELETING THE FILES IN HADOOP

	hdfs dfs -cat /fa/sampleda.txt
	hdfs dfs -du /DD/exp.txt
	hdfs dfs -rmr /DD
	hdfs dfs -ls /
	
	___PIG___
	
	5.DISPLAYING THE DATA

	dataa = LOAD'/home/myhduser/Desktop/neww.csv'USING PigStorage(',') AS (id:chararray,name:chararray,dept:chararray);

	dump dataa;

	6.DESCRIBING AND EXPLAINING THE DATA IN PIG:

	describe dataa;

	explain dataa;

	7.ILLUSTRATE AND ORDER COMMAND -PIG

	illustrate dataa;

	orderdata = ORDER dataa BY dept DESC;

	dump orderdata;

	8.GROUP COMMAND IN PIG

	groupby = GROUP dataa by dept;

	dump groupby;
	 
	grouapall = GROUP dataa all;

	dump grouapall;

	9.FOREACH COMMAND IN PIG


	name = FOREACH dataa GENERATE name;

	dump name;


	10.LOADING AND DUMPING THE TEXT IN PIG


	data = LOAD'/home/myhduser/new.txt' AS (data:chararray);

	dump data;
	
	
	___HIVE___
	
	start-all.sh
	jps
	hive

	11. Table operation in hive

	CODING

	create table emp(id INT, name STRING, dept STRING, yoj INT, salary INT)
	ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';

	LOAD DATA LOCAL INPATH '/home/myhduser/Downloads/Book2.csv'
	OVERWRITE INTO TABLE emp;

	select *from emp;

	12. Describe Query in hive

	CODING

	describe emp;
	select *from emp;

	13. Displaying and deleting tables in hive

	CODING

	show tables;
	DROP TABLE IF EXISTS emp;	
		
        
        """
        return avail_lx
    
