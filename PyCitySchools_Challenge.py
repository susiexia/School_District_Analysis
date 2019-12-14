# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# ## Conclusion:
# 
#      After removing the ninth-grade math and reading scores from Thomas High School, it affact summary tables by slightly reducing the average scores and enomous decreasing for the passing percentage rate, including both passing percentage of math and reading score as well as overall passing percentage.
#         

# %%
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'School_District_Analysis'))
	print(os.getcwd())
except:
	pass

# %% [markdown]
#  ### Load the csv file and Read the raw data

# %%
import os
import pandas as pd
import numpy as np

school_data_to_load = os.path.join('Resources','schools_complete.csv')
student_data_to_load = os.path.join('Resources', 'students_complete.csv')

school_data_df = pd.read_csv(school_data_to_load)
student_data_df = pd.read_csv(student_data_to_load)

# %% [markdown]
#  ### Clean student_names, remove inappropriate prefixes and suffixes

# %%
prefixes_suffixes = ["Dr. ", "Mr. ","Ms. ", "Mrs. ", "Miss ", " MD", " DDS", " DVM", " PhD"]

for word in prefixes_suffixes:
    student_data_df['student_name'] = student_data_df['student_name'].str.replace(word,'')

student_data_df

# %% [markdown]
# ## Replace the reading and math scores for ninth graders at Thomas High School with NaN.
# 

# %%
# use loc function to filter 9th grade , retrieve seperated Thomas school's 9th information and make scores to NaN

Challenge_student_data_df = student_data_df.copy()

#Thomas_9th_df = Challenge_student_data_df.loc[(Challenge_student_data_df['grade'] == '9th')&(Challenge_student_data_df['school_name'] =='Thomas High School')]
#Thomas_9th_df.describe()

Challenge_student_data_df.loc[(Challenge_student_data_df['grade'] == '9th')&(Challenge_student_data_df['school_name'] =='Thomas High School'),'reading_score':'math_score'] = np.nan
Challenge_student_data_df.tail()

# %% [markdown]
# ### Merge Challenge_student_data with school dataset
# #### Create a combined dataframe named  'Challenge_school_data_complete_df ' l

# %%
Challenge_school_data_complete_df = pd.merge(Challenge_student_data_df, school_data_df, on=['school_name'])
Challenge_school_data_complete_df.tail()

# %% [markdown]
# ### Compare with original non-clean merged dataframe 
# 

# %%
school_data_complete_df = pd.merge(student_data_df,school_data_df, on=['school_name'])
school_data_complete_df.tail()

# %% [markdown]
#  # TABLE No.1:   A high level snapshot of district's key metircs
# 
# %% [markdown]
# ### Analysis:
# * There is a slightly impact to this high level snapshot summary.
# By comparing two district sammary table, there is no change in columns of 'Total Schools','Total Students' and 'Total Budget'. All of percentage metrics( % Passing Math, % Passing Reading and % Overall Passing) and Average Math score are slightly lower than original table.
#       
#       
# %% [markdown]
# ### Challenge data _ clean

# %%
# calculate key metrics
C_student_count = Challenge_school_data_complete_df.student_name.count()
C_school_count = len(Challenge_school_data_complete_df.school_name.unique())
C_total_budget = school_data_df.budget.agg('sum') 
C_avg_math = Challenge_school_data_complete_df.math_score.agg('mean')
C_avg_reading = Challenge_school_data_complete_df.reading_score.mean()

pass_math_filter_df = Challenge_school_data_complete_df[Challenge_school_data_complete_df.math_score >= 70]
pass_reading_filter_df = Challenge_school_data_complete_df[Challenge_school_data_complete_df.reading_score >= 70]

passing_math_count = pass_math_filter_df.student_name.count()
passing_reading_count = pass_reading_filter_df.student_name.count()

C_passing_math_percentage = passing_math_count/float(C_student_count)*100

C_passing_reading_percentage = passing_reading_count/float(C_student_count)*100

C_overall_passing_percentage = (C_passing_math_percentage + C_passing_reading_percentage) /2

# put calculate outcomes into a summary dataframe
Challenge_district_summary_df = pd.DataFrame([{"Total Schools": C_school_count,
                      "Total Students": C_student_count,
                      "Total Budget": C_total_budget,
                      "Average Math Score": C_avg_math,
                      "Average Reading Score": C_avg_reading,
                      "% Passing Math": C_passing_math_percentage,
                      "% Passing Reading": C_passing_reading_percentage,
                      "% Overall Passing": C_overall_passing_percentage}])

# format summary dataframe
Challenge_district_summary_df["Total Students"] = Challenge_district_summary_df["Total Students"].map("{:,}".format)
Challenge_district_summary_df["Total Budget"] = Challenge_district_summary_df["Total Budget"].map("${:,.2f}".format)
Challenge_district_summary_df["Average Math Score"] = Challenge_district_summary_df["Average Math Score"].map("{:.1f}".format)
Challenge_district_summary_df["Average Reading Score"] = Challenge_district_summary_df["Average Reading Score"].map("{:.1f}".format)
Challenge_district_summary_df["% Passing Math"] = Challenge_district_summary_df["% Passing Math"].map("{:.0f}".format)
Challenge_district_summary_df["% Passing Reading"] = Challenge_district_summary_df["% Passing Reading"].map("{:.0f}".format)
Challenge_district_summary_df["% Overall Passing"] = Challenge_district_summary_df["% Overall Passing"].map("{:.0f}".format)

Challenge_district_summary_df

# %% [markdown]
# ### Original data _ not clean

# %%
# calculate key metrics
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

passing_reading_percentage = passing_reading_count/student_count *100

overall_passing_percentage = (passing_math_percentage + passing_reading_percentage) /2

# put calculate outcomes into a summary dataframe
district_summary_df = pd.DataFrame([{"Total Schools": school_count,
                      "Total Students": student_count,
                      "Total Budget": total_budget,
                      "Average Math Score": avg_math,
                      "Average Reading Score": avg_reading,
                      "% Passing Math": passing_math_percentage,
                      "% Passing Reading": passing_reading_percentage,
                      "% Overall Passing": overall_passing_percentage}])
# format summary dataframe
district_summary_df["Total Students"] = district_summary_df["Total Students"].map("{:,}".format)
district_summary_df["Total Budget"] = district_summary_df["Total Budget"].map("${:,.2f}".format)
district_summary_df["Average Math Score"] = district_summary_df["Average Math Score"].map("{:.1f}".format)
district_summary_df["Average Reading Score"] = district_summary_df["Average Reading Score"].map("{:.1f}".format)
district_summary_df["% Passing Math"] = district_summary_df["% Passing Math"].map("{:.0f}".format)
district_summary_df["% Passing Reading"] = district_summary_df["% Passing Reading"].map("{:.0f}".format)
district_summary_df["% Overall Passing"] = district_summary_df["% Overall Passing"].map("{:.0f}".format)

district_summary_df

# %% [markdown]
#  # TABLE No.2: overview of key metrics for each school
# 
# %% [markdown]
# ## Analysis: 
# * There is a big impact on school-level summary.
# By comparing the Thomas High school performance in two school summary tables, there are no changes on some columns such as School Type, Total Students,Total School Budget as well as Per Student Budget for Thomas high school. But both average scores in math and reading are slightly decreasing. However, all of passing percentage metrics( % Passing Math, % Passing Reading and % Overall Passing) wildly decrease from around 90% into around 60%. The decreasing range is around 27%. 
# 
# %% [markdown]
# ### Challenge data _ clean

# %%
#use set_index() fuction get Series by school name as row labels

C_per_school_types_Series=school_data_df.set_index(['school_name']).type
C_per_school_size_Series=school_data_df.set_index(['school_name'])['size']
C_per_school_budget_Series=school_data_df.set_index(['school_name'])['budget']
C_per_school_capita_Series = C_per_school_budget_Series/C_per_school_size_Series

C_per_school_student_count_series = Challenge_school_data_complete_df['school_name'].value_counts()

# use groupby() fuction get Series by school name as row labels
C_per_school_grp_math = Challenge_school_data_complete_df.groupby(['school_name']).math_score.agg('mean')
C_per_school_grp_reading = Challenge_school_data_complete_df.groupby(['school_name']).reading_score.mean()

C_pass_math_filter_df = Challenge_school_data_complete_df[Challenge_school_data_complete_df.math_score >= 70]
C_pass_reading_filter_df = Challenge_school_data_complete_df[Challenge_school_data_complete_df.reading_score >= 70]

C_per_school_passingMath_grp_Series = C_pass_math_filter_df.groupby(['school_name']).count()['student_name']
C_per_school_passingReading_grp_Series = C_pass_reading_filter_df.groupby(['school_name']).count()['student_name']

C_per_school_passing_math = C_per_school_passingMath_grp_Series/C_per_school_size_Series * 100
C_per_school_passing_reading = C_per_school_passingReading_grp_Series/C_per_school_size_Series * 100
C_per_overall_passing_percentage = (C_per_school_passing_math + C_per_school_passing_reading) /2

# put Series into a new DataFrame
Challenge_per_school_summary_df = pd.DataFrame({'School Type': C_per_school_types_Series,
                                                'Total Students': C_per_school_size_Series,
                                                'Total School Budget': C_per_school_budget_Series.map('${:,.2f}'.format),
                                                'Per Student Budget': C_per_school_capita_Series.map('${:,.2f}'.format),
                                                'Average Math Score': C_per_school_grp_math,
                                                'Average Reading Score': C_per_school_grp_reading,
                                                '% Passing Math': C_per_school_passing_math,
                                                '% Passing Reading': C_per_school_passing_reading,
                                                '% Overall Passing': C_per_overall_passing_percentage})
                     
Challenge_per_school_summary_df.tail()                                                                                                                                                                                    

# %% [markdown]
# ### Original data _ not clean

# %%
#use set_index() fuction, retrieve school name as row labels

per_school_types_Series=school_data_df.set_index(['school_name']).type
per_school_size_Series=school_data_df.set_index(['school_name'])['size']
per_school_budget_Series=school_data_df.set_index(['school_name'])['budget']
per_school_capita_Series = per_school_budget_Series/per_school_size_Series

per_school_student_count_series = school_data_complete_df.school_name.value_counts()

# use groupby() fuction get Series by school name as row labels
per_school_grp_math = school_data_complete_df.groupby(['school_name']).math_score.agg('mean')
per_school_grp_reading = school_data_complete_df.groupby(['school_name']).reading_score.mean()

pass_math_filter_df = school_data_complete_df[school_data_complete_df.math_score >= 70]
pass_reading_filter_df = school_data_complete_df[school_data_complete_df.reading_score >= 70]

per_school_passingMath_grp_Series = pass_math_filter_df.groupby(['school_name']).count()['student_name']
per_school_passingReading_grp_Series = pass_reading_filter_df.groupby(['school_name']).count()['student_name']

per_school_passing_math = per_school_passingMath_grp_Series/per_school_size_Series * 100
per_school_passing_reading = per_school_passingReading_grp_Series/per_school_size_Series * 100
per_overall_passing_percentage = (per_school_passing_math + per_school_passing_reading) /2

# put Series into a new DataFrame
per_school_summary_df = pd.DataFrame({'School Type': per_school_types_Series,
                                      'Total Students': per_school_size_Series,
                                      'Total School Budget': per_school_budget_Series.map('${:,.2f}'.format),
                                      'Per Student Budget': per_school_capita_Series.map('${:,.2f}'.format),
                                      'Average Math Score': per_school_grp_math,
                                      'Average Reading Score': per_school_grp_reading,
                                      '% Passing Math': per_school_passing_math,
                                      '% Passing Reading': per_school_passing_reading,
                                      '% Overall Passing': per_overall_passing_percentage})                       
per_school_summary_df.tail()                                                                                                                                                                                     

# %% [markdown]
#  # TABLE No.3 Top 5 and bottom 5 performing schools, based on the overall passing rate
# 
# %% [markdown]
# ## Analysis:
# * After removing the ninth graders’ math and reading scores, the rank of Thomas High School drops from top 5 to bottom 5 schools based on overall passing percentage. Before removing incorrect score, Thomas High School is No.2 with 95.29% overall passing rate. Now, Thomas High School is the last one with 68% overall passing rate
# %% [markdown]
# ### Challenge data _ clean

# %%
Challenge_top_schools_df = Challenge_per_school_summary_df.sort_values(['% Overall Passing'], ascending = False)
Challenge_top_schools_df.head()


# %%
Challenge_bottom_schools_df = Challenge_per_school_summary_df.sort_values(['% Overall Passing'])
Challenge_bottom_schools_df.head()

# %% [markdown]
# ### Original data _ not clean

# %%
top_schools_df = per_school_summary_df.sort_values(['% Overall Passing'], ascending = False)
top_schools_df.head()


# %%
bottom_schools_df = per_school_summary_df.sort_values(['% Overall Passing'])
bottom_schools_df.head()

# %% [markdown]
#  # TABLE No.4: The average math score received by students in each grade level at each school
# 
# %% [markdown]
# ## Analysis:
# * After removing the ninth graders’ math scores, we can see the table shows 'NaN' for the value of 9th grade in Thomas High school. Beside that, other value in table keeps no change comparing with original table.
# %% [markdown]
# ### Challenge data _ clean

# %%
# filter DataFrame for each grade level by different grade 
C_complete_9th_filtered_df = Challenge_school_data_complete_df[(Challenge_school_data_complete_df.grade == '9th')]
C_complete_10th_filtered_df = Challenge_school_data_complete_df[(Challenge_school_data_complete_df.grade == '10th')]
C_complete_11th_filtered_df = Challenge_school_data_complete_df[(Challenge_school_data_complete_df.grade == '11th')]
C_complete_12th_filtered_df = Challenge_school_data_complete_df[(Challenge_school_data_complete_df.grade == '12th')]


#retrieve average math and reeading score Series groupby school name
C_grade9th_math_school_grp_Series = C_complete_9th_filtered_df.groupby(['school_name']).mean()['math_score']
C_grade10th_math_school_grp_Series = C_complete_10th_filtered_df.groupby(['school_name']).mean()['math_score']
C_grade11th_math_school_grp_Series = C_complete_11th_filtered_df.groupby(['school_name']).mean()['math_score']
C_grade12th_math_school_grp_Series = C_complete_12th_filtered_df.groupby(['school_name']).mean()['math_score']

C_grade9th_reading_school_grp_Series = C_complete_9th_filtered_df.groupby(['school_name']).mean()['reading_score']
C_grade10th_reading_school_grp_Series = C_complete_10th_filtered_df.groupby(['school_name']).mean()['reading_score']
C_grade11th_reading_school_grp_Series = C_complete_11th_filtered_df.groupby(['school_name']).mean()['reading_score']
C_grade12th_reading_school_grp_Series = C_complete_12th_filtered_df.groupby(['school_name']).mean()['reading_score']

#Create a new DataFrame for average math score received by students in each grade level at each school
Challenge_grade_math_summary_df = pd.DataFrame({'9th':C_grade9th_math_school_grp_Series.map('{:.1f}'.format),
                            '10th':C_grade10th_math_school_grp_Series.map('{:.1f}'.format),
                            '11th':C_grade11th_math_school_grp_Series.map('{:.1f}'.format),
                            '12th':C_grade12th_math_school_grp_Series.map('{:.1f}'.format)})
# remove index column's name
Challenge_grade_math_summary_df.index.name = None
Challenge_grade_math_summary_df

# %% [markdown]
# ### Original data _ not clean

# %%
# filter DataFrame for each grade level by different grade 
complete_9th_filtered_df = school_data_complete_df[(school_data_complete_df.grade == '9th')]
complete_10th_filtered_df = school_data_complete_df[(school_data_complete_df.grade == '10th')]
complete_11th_filtered_df = school_data_complete_df[(school_data_complete_df.grade == '11th')]
complete_12th_filtered_df = school_data_complete_df[(school_data_complete_df.grade == '12th')]


#retrieve average math and reeading score Series groupby school name
grade9th_math_school_grp_Series = complete_9th_filtered_df.groupby(['school_name']).mean()['math_score']
grade10th_math_school_grp_Series = complete_10th_filtered_df.groupby(['school_name']).mean()['math_score']
grade11th_math_school_grp_Series = complete_11th_filtered_df.groupby(['school_name']).mean()['math_score']
grade12th_math_school_grp_Series = complete_12th_filtered_df.groupby(['school_name']).mean()['math_score']

grade9th_reading_school_grp_Series = complete_9th_filtered_df.groupby(['school_name']).mean()['reading_score']
grade10th_reading_school_grp_Series = complete_10th_filtered_df.groupby(['school_name']).mean()['reading_score']
grade11th_reading_school_grp_Series = complete_11th_filtered_df.groupby(['school_name']).mean()['reading_score']
grade12th_reading_school_grp_Series = complete_12th_filtered_df.groupby(['school_name']).mean()['reading_score']

#Create a new DataFrame for average math score received by students in each grade level at each school
grade_math_summary_df = pd.DataFrame({'9th':grade9th_math_school_grp_Series.map('{:.1f}'.format),
                            '10th':grade10th_math_school_grp_Series.map('{:.1f}'.format),
                            '11th':grade11th_math_school_grp_Series.map('{:.1f}'.format),
                            '12th':grade12th_math_school_grp_Series.map('{:.1f}'.format)})
# remove index column's name
grade_math_summary_df.index.name = None
grade_math_summary_df

# %% [markdown]
#  # TABLE No.5: The average reading score received by students in each grade level at each school
# 
# %% [markdown]
# ## Analysis:
# * After removing the ninth graders’ reading scores, there is no change except 'NaN' value showing for 9th grade of Thomas High school.
# %% [markdown]
# ### Challenge data _ clean

# %%
#Create a new DataFrame for average math score received by students in each grade level at each school
Challenge_grade_reading_summary_df = pd.DataFrame({'9th':C_grade9th_reading_school_grp_Series.map('{:.1f}'.format),
                            '10th':C_grade10th_reading_school_grp_Series.map('{:.1f}'.format),
                            '11th':C_grade11th_reading_school_grp_Series.map('{:.1f}'.format),
                            '12th':C_grade12th_reading_school_grp_Series.map('{:.1f}'.format)})
Challenge_grade_reading_summary_df.index.name = None                            
Challenge_grade_reading_summary_df

# %% [markdown]
# ### Original data _ not clean

# %%
#Create a new DataFrame for average math score received by students in each grade level at each school
grade_reading_summary_df = pd.DataFrame({'9th':grade9th_reading_school_grp_Series.map('{:.1f}'.format),
                            '10th':grade10th_reading_school_grp_Series.map('{:.1f}'.format),
                            '11th':grade11th_reading_school_grp_Series.map('{:.1f}'.format),
                            '12th':grade12th_reading_school_grp_Series.map('{:.1f}'.format)})
grade_reading_summary_df.index.name = None                            
grade_reading_summary_df

# %% [markdown]
#  # TABLE No.6: School performance based on the budget per student
#  
# %% [markdown]
# ## Analysis:
# * Because Thomas High school is in the spending range of '630-644', there is no change in other three bins. In the'630-644' range, the three passing percentage metrics: ("% Passing Math", "% Passing Reading" and "% Overall Passing") decline by 6-7%. However, There are very slightly impact on average math and reading score for the'630-644' range. For example, the original average math score is 78.518855, after removing incorrect data, average math score is 78.502002. In that case, we will ignore this difference by formatting average scores rounded to the nearest tenth. 
# 
# %% [markdown]
# ### Challenge data _ clean

# %%
#create four fairly spending bins
spending_bins = [0,585,630,645,675]
group_names = ["<$584", "$585-629", "$630-644", "$645-675"]
#cut budget per student Series into 4 bins, and labeled as group_names
C_cutted_capita_categorical_S = pd.cut(C_per_school_capita_Series,spending_bins, labels=group_names)

# add 'Spending Ranges(per student)'Series into dataframe
Challenge_per_school_summary_df['Spending Ranges (Per Student)'] = pd.Series(C_cutted_capita_categorical_S)

#retrieve Series groupby 'Spending Ranges(per student)' in the same dataframe
C_spending_math_scores_Series = Challenge_per_school_summary_df.groupby(['Spending Ranges (Per Student)'])['Average Math Score'].agg('mean')
C_spending_reading_scores_Series = Challenge_per_school_summary_df.groupby(['Spending Ranges (Per Student)'])['Average Reading Score'].agg('mean')
C_spending_passing_math_Series =Challenge_per_school_summary_df.groupby(['Spending Ranges (Per Student)'])['% Passing Math'].agg('mean')
C_spending_passing_reading_Series =Challenge_per_school_summary_df.groupby(['Spending Ranges (Per Student)'])['% Passing Reading'].agg('mean')
C_Spending_overall_passing_percentage_Series = (C_spending_passing_math_Series + C_spending_passing_reading_Series) /2

# add Series into a new dataframe, row label as 'Spending Ranges(per student)'
Challenge_spending_school_summary_df = pd.DataFrame({"Average Math Score" : C_spending_math_scores_Series.map('{:.1f}'.format),
          "Average Reading Score": C_spending_reading_scores_Series.map('{:.1f}'.format),
          "% Passing Math": C_spending_passing_math_Series.map('{:.0f}'.format),
          "% Passing Reading": C_spending_passing_reading_Series.map('{:.0f}'.format),
          "% Overall Passing": C_Spending_overall_passing_percentage_Series.map('{:.0f}'.format)})

Challenge_spending_school_summary_df

# %% [markdown]
# ### Original data _ not clean

# %%
#create four fairly spending bins
spending_bins = [0,585,630,645,675]
group_names = ["<$584", "$585-629", "$630-644", "$645-675"]
#cut budget per student Series into 4 bins, and labeled as group_names
cutted_capita_categorical_S = pd.cut(per_school_capita_Series,spending_bins, labels=group_names)

# add 'Spending Ranges(per student)'Series into dataframe
per_school_summary_df['Spending Ranges (Per Student)'] = pd.Series(cutted_capita_categorical_S)

#retrieve Series groupby 'Spending Ranges(per student)' in the same dataframe
spending_math_scores_Series = per_school_summary_df.groupby(['Spending Ranges (Per Student)'])['Average Math Score'].agg('mean')
spending_reading_scores_Series = per_school_summary_df.groupby(['Spending Ranges (Per Student)'])['Average Reading Score'].agg('mean')
spending_passing_math_Series =per_school_summary_df.groupby(['Spending Ranges (Per Student)'])['% Passing Math'].agg('mean')
spending_passing_reading_Series =per_school_summary_df.groupby(['Spending Ranges (Per Student)'])['% Passing Reading'].agg('mean')
Spending_overall_passing_percentage_Series = (spending_passing_math_Series + spending_passing_reading_Series) /2

# add Series into a new dataframe, row label as 'Spending Ranges(per student)'
spending_school_summary_df = pd.DataFrame({"Average Math Score" : spending_math_scores_Series.map('{:.1f}'.format),
          "Average Reading Score": spending_reading_scores_Series.map('{:.1f}'.format),
          "% Passing Math": spending_passing_math_Series.map('{:.0f}'.format),
          "% Passing Reading": spending_passing_reading_Series.map('{:.0f}'.format),
          "% Overall Passing": Spending_overall_passing_percentage_Series.map('{:.0f}'.format)})

spending_school_summary_df

# %% [markdown]
#  # TABLE No.7: School performance based on the school size
# 
# %% [markdown]
# ## Analysis:
# * Thomas High school is in the medium range based on school size, . As a result, only metrics in medium size will change. The three passing percentage metrics: ("% Passing Math", "% Passing Reading" and "% Overall Passing") are decreasing around 5-6%. However, There are also a very slightly change in average math and reading score for medium range. We can ignore the difference by formatting average scores rounded to the nearest tenth. 
# %% [markdown]
# ### Challenge data _ clean

# %%
#create three size bins, and cut total students Series into 3 bins, and labeled as size_bins_labels
size_bins = [0, 1000, 2000, 5000]
size_bins_labels = ['Small(<1000)','Medium (1000-2000)','Large (2000-5000)']
C_cutted_size_categorical_S = pd.cut( Challenge_per_school_summary_df['Total Students'],size_bins, labels= size_bins_labels)

# add 'School Size Bins' Series into dataframe
Challenge_per_school_summary_df['School Size Bins'] = pd.Series(C_cutted_size_categorical_S)

#retrieve Series groupby 'School Size Bins' in the same dataframe
C_sizeBins_math_scores_Series = Challenge_per_school_summary_df.groupby(['School Size Bins'])['Average Math Score'].agg('mean')
C_sizeBins_reading_scores_Series = Challenge_per_school_summary_df.groupby(['School Size Bins'])['Average Reading Score'].agg('mean')
C_sizeBins_passing_math_Series = Challenge_per_school_summary_df.groupby(['School Size Bins'])['% Passing Math'].agg('mean')
C_sizeBins_passing_reading_Series = Challenge_per_school_summary_df.groupby(['School Size Bins'])['% Passing Reading'].agg('mean')
C_sizeBins_overall_passing_percentage_Series = (C_sizeBins_passing_math_Series + C_sizeBins_passing_reading_Series) /2

# add Series into a new dataframe, row labels as 'School Size Bins'
Challenge_size_school_summary_df = pd.DataFrame({"Average Math Score" : C_sizeBins_math_scores_Series.map('{:.1f}'.format),
          "Average Reading Score": C_sizeBins_reading_scores_Series.map('{:.1f}'.format),
          "% Passing Math": C_sizeBins_passing_math_Series.map('{:.0f}'.format),
          "% Passing Reading": C_sizeBins_passing_reading_Series.map('{:.0f}'.format),
          "% Overall Passing": C_sizeBins_overall_passing_percentage_Series.map('{:.0f}'.format)})

Challenge_size_school_summary_df

# %% [markdown]
# ### Original data _ not clean

# %%
#create three size bins, and cut total students Series into 3 bins, and labeled as size_bins_labels
size_bins = [0, 1000, 2000, 5000]
size_bins_labels = ['Small(<1000)','Medium (1000-2000)','Large (2000-5000)']
cutted_size_categorical_S = pd.cut( per_school_summary_df['Total Students'],size_bins, labels= size_bins_labels)

# add 'School Size Bins' Series into dataframe
per_school_summary_df['School Size Bins'] = pd.Series(cutted_size_categorical_S)

#retrieve Series groupby 'School Size Bins' in the same dataframe
sizeBins_math_scores_Series = per_school_summary_df.groupby(['School Size Bins'])['Average Math Score'].agg('mean')
sizeBins_reading_scores_Series = per_school_summary_df.groupby(['School Size Bins'])['Average Reading Score'].agg('mean')
sizeBins_passing_math_Series = per_school_summary_df.groupby(['School Size Bins'])['% Passing Math'].agg('mean')
sizeBins_passing_reading_Series = per_school_summary_df.groupby(['School Size Bins'])['% Passing Reading'].agg('mean')
sizeBins_overall_passing_percentage_Series = (sizeBins_passing_math_Series + sizeBins_passing_reading_Series) /2

# add Series into a new dataframe, row labels as 'School Size Bins'
size_school_summary_df = pd.DataFrame({"Average Math Score" : sizeBins_math_scores_Series.map('{:.1f}'.format),
          "Average Reading Score": sizeBins_reading_scores_Series.map('{:.1f}'.format),
          "% Passing Math": sizeBins_passing_math_Series.map('{:.0f}'.format),
          "% Passing Reading": sizeBins_passing_reading_Series.map('{:.0f}'.format),
          "% Overall Passing": sizeBins_overall_passing_percentage_Series.map('{:.0f}'.format)})

size_school_summary_df

# %% [markdown]
#  # TABLE No.8: School performance based on the type of school
# 
# %% [markdown]
# ## Analysis:
# * The school type of Thomas High school is Charter, only performance metrics for charter type changes. The "% Passing Math" and "% Passing Reading" reduce 4% comparing to original table. and "% Overall Passing" is decreasing by 3%. However, There are also a very slightly change in average math and reading score for Charter. We can ignore the difference by formatting average scores rounded to the nearest tenth.
# %% [markdown]
# ### Challenge data _ clean

# %%
#retrieve Series groupby 'School Type' in the same dataframe
C_type_math_scores_Series = Challenge_per_school_summary_df.groupby(["School Type"]).mean()["Average Math Score"]
C_type_reading_scores_Series = Challenge_per_school_summary_df.groupby(["School Type"]).mean()["Average Reading Score"]
C_type_passing_math_Series = Challenge_per_school_summary_df.groupby(["School Type"]).mean()["% Passing Math"]
C_type_passing_reading_Series = Challenge_per_school_summary_df.groupby(["School Type"]).mean()["% Passing Reading"]
C_type_overall_passing_Series = (C_type_passing_math_Series + C_type_passing_reading_Series) / 2

# add Series into a new dataframe, row labels as 'School Type
Challenge_type_school_summary_df = pd.DataFrame({"Average Math Score" : C_type_math_scores_Series.map('{:.1f}'.format),
          "Average Reading Score": C_type_reading_scores_Series.map('{:.1f}'.format),
          "% Passing Math": C_type_passing_math_Series.map('{:.0f}'.format),
          "% Passing Reading": C_type_passing_reading_Series.map('{:.0f}'.format),
          "% Overall Passing": C_type_overall_passing_Series.map('{:.0f}'.format)})

Challenge_type_school_summary_df

# %% [markdown]
# ### Original data _ not clean

# %%
#retrieve Series groupby 'School Type' in the same dataframe
type_math_scores_Series = per_school_summary_df.groupby(["School Type"]).mean()["Average Math Score"]
type_reading_scores_Series = per_school_summary_df.groupby(["School Type"]).mean()["Average Reading Score"]
type_passing_math_Series = per_school_summary_df.groupby(["School Type"]).mean()["% Passing Math"]
type_passing_reading_Series = per_school_summary_df.groupby(["School Type"]).mean()["% Passing Reading"]
type_overall_passing_Series = (type_passing_math_Series + type_passing_reading_Series) / 2

# add Series into a new dataframe, row labels as 'School Type'
type_school_summary_df = pd.DataFrame({"Average Math Score" : type_math_scores_Series.map('{:.1f}'.format),
          "Average Reading Score": type_reading_scores_Series.map('{:.1f}'.format),
          "% Passing Math": type_passing_math_Series.map('{:.0f}'.format),
          "% Passing Reading": type_passing_reading_Series.map('{:.0f}'.format),
          "% Overall Passing": type_overall_passing_Series.map('{:.0f}'.format)})

type_school_summary_df

# %% [markdown]
# ## Compare the final per_school_summary dataframes:

# %%
Challenge_per_school_summary_df.tail()


# %%
per_school_summary_df.tail()


# %%


