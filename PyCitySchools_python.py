# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
#import os
#try:
	#os.chdir(os.path.join(os.getcwd(), 'School_District_Analysis'))
	#print(os.getcwd())
#except:
	#pass
# %%
#use os.path.join(), indirectly load file
#use Pandas.read_csv to read (without open files) into DataFrame


# %%
import os
import pandas as pd

school_data_to_load = os.path.join('Resources','schools_complete.csv')
student_data_to_load = os.path.join('Resources', 'students_complete.csv')

school_data_df = pd.read_csv(school_data_to_load)
student_data_df = pd.read_csv(student_data_to_load)


# %%

print(student_data_df.head())
student_data_df.tail(10)
student_data_df.describe()

# %%
school_data_df.head()
# %%
student_data_df.count()


# %%
school_data_df.isnull()


# %%
student_data_df.isnull().sum()


# %%
student_data_df.notnull().sum()


# %%
#use _df.dropna() & _df.fillna(0) to deal with missing data


# %%
#check data types, !! Attribute
school_data_df.dtypes


# %%
student_data_df.dtypes


# %%
student_data_df.grade.dtype
student_data_df['reading_score'].dtype


# %%
# clean incorrect student names
prefixes_suffixes = ["Dr. ", "Mr. ","Ms. ", "Mrs. ", "Miss ", " MD", " DDS", " DVM", " PhD"]

for word in prefixes_suffixes:
    student_data_df['student_name'] = student_data_df['student_name'].str.replace(word,'')
print(student_data_df.head(10))

# %% [markdown]
# ### merge two dataFrame
# 

# %%
#check two DataFrame columns
print(student_data_df.columns)
print(len(school_data_df.columns))


# %%
#merge school_data_df(right) and student_data_df(left) on a shared column 'school_name'

school_data_complete_df = pd.merge(student_data_df,school_data_df, on=['school_name'])
school_data_complete_df.head()

# %% [markdown]
# ### calculate key metrics for new merged DataFrame

# %%
student_count = school_data_complete_df.student_name.count()
school_count = len(school_data_complete_df.school_name.unique())
total_budget = school_data_df.budget.agg('sum')  #use origal school DataFrame
avg_math = school_data_complete_df.math_score.agg('mean')
avg_reading = school_data_complete_df.reading_score.mean()

pass_math_filter_df = school_data_complete_df[school_data_complete_df.math_score >= 70]
pass_reading_filter_df = school_data_complete_df[school_data_complete_df.reading_score >= 70]
passing_math_count = pass_math_filter_df.student_name.count()
passing_reading_count = pass_reading_filter_df.student_name.count()

passing_math_percentage = passing_math_count/float(student_count)*100
print('Math pass Rate: ',passing_math_percentage)
passing_reading_percentage = passing_reading_count/student_count *100
print('Readinf pass Rate: ',passing_reading_percentage)
overall_passing_percentage = (passing_math_percentage + passing_reading_percentage) /2
print(f'Overall pass Rate:{overall_passing_percentage:.2f}%')

# %% [markdown]
# ### a summary new Dataframe to collect all key metrics aboved

# %%
district_summary_df = pd.DataFrame([{"Total Schools": school_count,
                      "Total Students": student_count,
                      "Total Budget": total_budget,
                      "Average Math Score": avg_math,
                      "Average Reading Score": avg_reading,
                      "% Passing Math": passing_math_percentage,
                      "% Passing Reading": passing_reading_percentage,
                      "% Overall Passing": overall_passing_percentage}])
district_summary_df

# %% [markdown]
# ### Format summary DataFrame by using map("{}".format) |||| map and format chaining

# %%
district_summary_df["Total Students"] = district_summary_df["Total Students"].map("{:,}".format)
district_summary_df["Total Budget"] = district_summary_df["Total Budget"].map("${:,.2f}".format)
district_summary_df["Average Math Score"] = district_summary_df["Average Math Score"].map("{:.1f}".format)
district_summary_df["Average Reading Score"] = district_summary_df["Average Reading Score"].map("{:.1f}".format)
district_summary_df["% Passing Math"] = district_summary_df["% Passing Math"].map("{:.0f}".format)
district_summary_df["% Passing Reading"] = district_summary_df["% Passing Reading"].map("{:.0f}".format)
district_summary_df["% Overall Passing"] = district_summary_df["% Overall Passing"].map("{:.0f}".format)

district_summary_df

# %% [markdown]
# ## Table: overview of key metrics for each school |||| school name as index 

# %%
#retrieve school name as row labels, school type as the first column, to make a new DataFrame

per_school_types_Series=school_data_df.set_index(['school_name']).type


#or: per_school_summary_df = pd.DataFrame({'school_type':per_school_types_Series})
per_school_summary_df = pd.DataFrame(per_school_types_Series)

per_school_summary_df

# %% [markdown]
# #### very useful column method: to get frequency of every value appeared, same results as .set_index() method
# #### in a descending order

# %%

per_school_student_count_series = school_data_complete_df.school_name.value_counts()
per_school_student_count_series


# %%
per_school_size_Series=school_data_df.set_index(['school_name'])['size']
per_school_size_Series


# %%
per_school_budget_Series=school_data_df.set_index(['school_name'])['budget']
per_school_budget_Series

# %%
per_school_capita_Series = per_school_budget_Series/per_school_size_Series
per_school_capita_Series

# %%
F_per_school_capita_Series = per_school_capita_Series.map('${:.0f}'.format)
F_per_school_capita_Series

# %% [markdown]
# #### groupby()
# %%
per_school_grp_math = school_data_complete_df.groupby(['school_name']).math_score.agg('mean')
per_school_grp_reading = school_data_complete_df.groupby(['school_name']).reading_score.mean()
per_school_grp_math
per_school_grp_reading
# %% 
# groupby two Series 
per_school_student_grp_df = school_data_complete_df.groupby(by=['school_name','student_name'], axis = 0, as_index = False).mean()

# %%[markdown]
# #### groupby() and percentage
# %%
pass_math_filter_df = school_data_complete_df[school_data_complete_df.math_score >= 70]
pass_reading_filter_df = school_data_complete_df[school_data_complete_df.reading_score >= 70]

per_school_passingMath_grp_Series = pass_math_filter_df.groupby(['school_name']).count()['student_name']
per_school_passingReading_grp_Series = pass_reading_filter_df.groupby(['school_name']).count()['student_name']
per_school_passingReading_grp_Series

per_school_passing_math = per_school_passingMath_grp_Series/per_school_size_Series * 100
per_school_passing_reading = per_school_passingReading_grp_Series/per_school_size_Series * 100
per_overall_passing_percentage = (per_school_passing_math + per_school_passing_reading) /2
per_overall_passing_percentage

# %%[markdown]
# #### New DataFrame of key metrics for per_school_summary_df
# ##### This summary dont need to groupby or set_index, because all Columns are index by school_name !!!

# %%
per_school_summary_df = pd.DataFrame({'Total Students': per_school_size_Series,
                                      'Total School Budget': per_school_budget_Series.map('${:,.2f}'.format),
                                      'Per Student Budget': per_school_capita_Series.map('${:,.2f}'.format),
                                      'Average Math Score': per_school_grp_math,
                                      'Average Reading Score': per_school_grp_reading,
                                      '% Passing Math': per_school_passing_math,
                                      '% Passing Reading': per_school_passing_reading,
                                      '% Overall Passing': per_overall_passing_percentage})

# %%
per_school_summary_df['School Type'] = pd.Series(per_school_types_Series)
per_school_column_reorder = ['School Type','Total Students','Total School Budget','Per Student Budget',
                            'Average Math Score','Average Reading Score','% Passing Math','% Passing Reading',
                            '% Overall Passing' ]
per_school_summary_df = per_school_summary_df[per_school_column_reorder]                        
per_school_summary_df.head()                                                                                                                                                                                     

# %% [markdown]
# ###Find out highest and lowest perforance sort_values()