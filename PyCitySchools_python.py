# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% 
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'School_District_Analysis'))
	print(os.getcwd())
except:
	pass
# %% [markdown]
# ## Load the csv file and Read the raw data

# %%
import os
import pandas as pd

school_data_to_load = os.path.join('Resources','schools_complete.csv')
student_data_to_load = os.path.join('Resources', 'students_complete.csv')

school_data_df = pd.read_csv(school_data_to_load)
student_data_df = pd.read_csv(student_data_to_load)


# %%

student_data_df.head()

# %%
school_data_df.head()

# %% [markdown]
# ## Clean student_names, remove inappropriate prefixes and suffixes

# %%
prefixes_suffixes = ["Dr. ", "Mr. ","Ms. ", "Mrs. ", "Miss ", " MD", " DDS", " DVM", " PhD"]

for word in prefixes_suffixes:
    student_data_df['student_name'] = student_data_df['student_name'].str.replace(word,'')
student_data_df.head(10)

# %% [markdown]
# # TABLE No.1: A high level snapshot of district's key metircs
# ## district_summary_df

# %%
#Merge school_data_df(right) and student_data_df(left) on a shared column 'school_name'

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
# ### A summary new Dataframe to collect all key metrics generated 

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
# # TABLE No.2: overview of key metrics for each school 
# ## per_school_summary_df

# %%
#retrieve school name as row labels, school type as the first column, to make a new DataFrame
#use set_index() fuction

per_school_types_Series=school_data_df.set_index(['school_name']).type

per_school_summary_df = pd.DataFrame(per_school_types_Series)

# %%
per_school_student_count_series = school_data_complete_df.school_name.value_counts()

per_school_size_Series=school_data_df.set_index(['school_name'])['size']

per_school_budget_Series=school_data_df.set_index(['school_name'])['budget']

per_school_capita_Series = per_school_budget_Series/per_school_size_Series

# %%
# use groupby() fuction 
per_school_grp_math = school_data_complete_df.groupby(['school_name']).math_score.agg('mean')
per_school_grp_reading = school_data_complete_df.groupby(['school_name']).reading_score.mean()

pass_math_filter_df = school_data_complete_df[school_data_complete_df.math_score >= 70]
pass_reading_filter_df = school_data_complete_df[school_data_complete_df.reading_score >= 70]

per_school_passingMath_grp_Series = pass_math_filter_df.groupby(['school_name']).count()['student_name']
per_school_passingReading_grp_Series = pass_reading_filter_df.groupby(['school_name']).count()['student_name']

per_school_passing_math = per_school_passingMath_grp_Series/per_school_size_Series * 100
per_school_passing_reading = per_school_passingReading_grp_Series/per_school_size_Series * 100
per_overall_passing_percentage = (per_school_passing_math + per_school_passing_reading) /2

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
# # TABLE No.3 Top 5 and bottom 5 performing schools, based on the overall passing rate
# ## use sort_values()
# ## top_schools_df and bottom_schools_df
# %%
top_schools_df = per_school_summary_df.sort_values(['% Overall Passing'], ascending = False)
top_schools_df.head(5)
bottom_schools_df = per_school_summary_df.sort_values(['% Overall Passing'])
bottom_schools_df.head()
# %% [markdown]
# # TABLE No.4: The average math score received by students in each grade level at each school
# ## grade_math_summary_df

# %%
# filter different grade, create DF for each grade level
complete_9th_filtered_df = school_data_complete_df[(school_data_complete_df.grade == '9th')]
complete_10th_filtered_df = school_data_complete_df[(school_data_complete_df.grade == '10th')]
complete_11th_filtered_df = school_data_complete_df[(school_data_complete_df.grade == '11th')]
complete_12th_filtered_df = school_data_complete_df[(school_data_complete_df.grade == '12th')]

# %%

grade9th_math_school_grp_Series = complete_9th_filtered_df.groupby(['school_name']).mean()['math_score']
grade10th_math_school_grp_Series = complete_10th_filtered_df.groupby(['school_name']).mean()['math_score']
grade11th_math_school_grp_Series = complete_11th_filtered_df.groupby(['school_name']).mean()['math_score']
grade12th_math_school_grp_Series = complete_12th_filtered_df.groupby(['school_name']).mean()['math_score']

grade9th_reading_school_grp_Series = complete_9th_filtered_df.groupby(['school_name']).mean()['reading_score']
grade10th_reading_school_grp_Series = complete_10th_filtered_df.groupby(['school_name']).mean()['reading_score']
grade11th_reading_school_grp_Series = complete_11th_filtered_df.groupby(['school_name']).mean()['reading_score']
grade12th_reading_school_grp_Series = complete_12th_filtered_df.groupby(['school_name']).mean()['reading_score']


# %%
grade_math_summary_df = pd.DataFrame({'9th':grade9th_math_school_grp_Series.map('{:.1f}'.format),
                            '10th':grade10th_math_school_grp_Series.map('{:.1f}'.format),
                            '11th':grade11th_math_school_grp_Series.map('{:.1f}'.format),
                            '12th':grade12th_math_school_grp_Series.map('{:.1f}'.format)})
# remove index column's name
grade_math_summary_df.index.name = None
grade_math_summary_df
# %% [markdown]
# # TABLE No.5: The average reading score received by students in each grade level at each school
# ## grade_reading_summary_df
# %%
grade_reading_summary_df = pd.DataFrame({'9th':grade9th_reading_school_grp_Series.map('{:.1f}'.format),
                            '10th':grade10th_reading_school_grp_Series.map('{:.1f}'.format),
                            '11th':grade11th_reading_school_grp_Series.map('{:.1f}'.format),
                            '12th':grade12th_reading_school_grp_Series.map('{:.1f}'.format)})
grade_reading_summary_df.index.name = None                            
grade_reading_summary_df

# %% [markdown] 
# # TABLE No.6: School performance based on the budget per student
# ## use bins and cut() function to get spending_school_summary_df
# %%
spending_bins = [0,585,630,645,675]
group_names = ["<$584", "$585-629", "$630-644", "$645-675"]
cutted_capita_categorical_S = pd.cut(per_school_capita_Series,spending_bins, labels=group_names)

per_school_capita_Series_grp = per_school_capita_Series.groupby(cutted_capita_categorical_S).count()

#cutted_capita_categorical_S.value_counts()

per_school_summary_df['Spending Ranges (Per Student)'] = pd.Series(cutted_capita_categorical_S)
per_school_summary_df

# %%
spending_math_scores_Series = per_school_summary_df.groupby(['Spending Ranges (Per Student)'])['Average Math Score'].agg('mean')
spending_reading_scores_Series = per_school_summary_df.groupby(['Spending Ranges (Per Student)'])['Average Reading Score'].agg('mean')
spending_passing_math_Series =per_school_summary_df.groupby(['Spending Ranges (Per Student)'])['% Passing Math'].agg('mean')
spending_passing_reading_Series =per_school_summary_df.groupby(['Spending Ranges (Per Student)'])['% Passing Reading'].agg('mean')
Spending_overall_passing_percentage_Series = (spending_passing_math_Series + spending_passing_reading_Series) /2

spending_school_summary_df = pd.DataFrame({"Average Math Score" : spending_math_scores_Series.map('{:.1f}'.format),
          "Average Reading Score": spending_reading_scores_Series.map('{:.1f}'.format),
          "% Passing Math": spending_passing_math_Series.map('{:.0f}'.format),
          "% Passing Reading": spending_passing_reading_Series.map('{:.0f}'.format),
          "% Overall Passing": Spending_overall_passing_percentage_Series.map('{:.0f}'.format)})
spending_school_summary_df


# %% [markdown] 
# # TABLE No.7: School performance based on the school size
# ## size_school_summary_df

# %%
size_bins = [0, 1000, 2000, 5000]
size_bins_labels = ['Small(<1000)','Medium (1000-2000)','Large (2000-5000)']
cutted_size_categorical_S = pd.cut( per_school_summary_df['Total Students'],size_bins, labels= size_bins_labels)
per_school_summary_df['School Size Bins'] = pd.Series(cutted_size_categorical_S)

per_school_summary_df.head()


# %%
sizeBins_math_scores_Series = per_school_summary_df.groupby(['School Size Bins'])['Average Math Score'].agg('mean')
sizeBins_reading_scores_Series = per_school_summary_df.groupby(['School Size Bins'])['Average Reading Score'].agg('mean')
sizeBins_passing_math_Series = per_school_summary_df.groupby(['School Size Bins'])['% Passing Math'].agg('mean')
sizeBins_passing_reading_Series = per_school_summary_df.groupby(['School Size Bins'])['% Passing Reading'].agg('mean')
sizeBins_overall_passing_percentage_Series = (sizeBins_passing_math_Series + sizeBins_passing_reading_Series) /2

size_school_summary_df = pd.DataFrame({"Average Math Score" : sizeBins_math_scores_Series.map('{:.1f}'.format),
          "Average Reading Score": sizeBins_reading_scores_Series.map('{:.1f}'.format),
          "% Passing Math": sizeBins_passing_math_Series.map('{:.0f}'.format),
          "% Passing Reading": sizeBins_passing_reading_Series.map('{:.0f}'.format),
          "% Overall Passing": sizeBins_overall_passing_percentage_Series.map('{:.0f}'.format)})
size_school_summary_df

# %% [markdown] 
# # TABLE No.8: School performance based on the type of school
# ## type_school_summary_df
# %%
type_math_scores_Series = per_school_summary_df.groupby(["School Type"]).mean()["Average Math Score"]
type_reading_scores_Series = per_school_summary_df.groupby(["School Type"]).mean()["Average Reading Score"]
type_passing_math_Series = per_school_summary_df.groupby(["School Type"]).mean()["% Passing Math"]
type_passing_reading_Series = per_school_summary_df.groupby(["School Type"]).mean()["% Passing Reading"]
type_overall_passing_Series = (type_passing_math_Series + type_passing_reading_Series) / 2

type_school_summary_df = pd.DataFrame({"Average Math Score" : type_math_scores_Series.map('{:.1f}'.format),
          "Average Reading Score": type_reading_scores_Series.map('{:.1f}'.format),
          "% Passing Math": type_passing_math_Series.map('{:.0f}'.format),
          "% Passing Reading": type_passing_reading_Series.map('{:.0f}'.format),
          "% Overall Passing": type_overall_passing_Series.map('{:.0f}'.format)})
type_school_summary_df
