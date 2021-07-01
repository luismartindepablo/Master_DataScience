###############################################
###############################################
# PEC4 PROGRAMACIÓN PARA LA CIENCIA DE DATOS
# Luis Martin - 31/5/2021
###############################################
###############################################

# Import modules
import utils
import pandas as pd
import matplotlib.pyplot as plt

# Create needed folders
utils.create_folder("figures")


#############
# EJERCICIO 1
#############
# Set arguments
file = "./data/covid_approval_polls.csv"
pattern1 = r"Huffington Post"
pattern2 = r"https?://\S*/([^/]+)\.pdf"
# Output exemples
utils.count_patterns(pattern1, file)
utils.count_patterns(pattern2, file)

# La función count_patterns carga el fichero linea a linea para no sobrecargar la memoria RAM.
# En el caso de tener archivos de 1Gb no tendríamos ningún problema en usar esta misma función.
# En el caso de tener 100 archivos de 1Gb deberíamos recurrir a programación concurrente.
# Utilizar programación en paralelo no supondria una mejora dado que leer un archivo no consume
# excesiva CPU.


#############
# EJERCICIO 2
#############
# Set arguments
dataset1 = pd.read_csv("./data/covid_approval_polls.csv")
dataset2 = pd.read_csv("./data/covid_concern_polls.csv")
pollsters = pd.read_excel("./data/pollster_ratings.xlsx", index_col=0)
output_name1 = "approval_polls.csv"
output_name2 = "concern_polls.csv"
# Create clean tables
utils.clean_dataset(dataset1, pollsters, output_name1)
utils.clean_dataset(dataset2, pollsters, output_name2)

# Dado que el tamaño de los archivos no es excesivamente grande y el tratamiento/análisis posterior
# al que se quiere someter los datos, el uso de la libreria pandas es el mas adecuado.


#############
# EJERCICIO 3
#############
# Read datasets
approval_polls = pd.read_csv("./data/approval_polls.csv")
# Filter dataset
word1 = "Trump"; word2 = "coronavirus"
pattern = r"(?=.*" + word1 + ")(?=.*" + word2 + ")"
approval_polls_filt = utils.pattern_search(pattern, approval_polls, "text")
# Calculate total people
approval_polls_filt["TotalApprove"] = approval_polls_filt.approve * approval_polls_filt.sample_size / 100
approval_polls_filt["TotalDisapprove"] = approval_polls_filt.disapprove * approval_polls_filt.sample_size / 100
# Groupby
approvalByParty = approval_polls_filt.groupby(by="party")
Total = approvalByParty.sum()[["TotalApprove", "TotalDisapprove"]]
# Plot
Total.plot(kind="bar")
plt.title("Approval Polls")
plt.ylabel("Count"); plt.xlabel("Party")
plt.savefig("./figures/Ejercicio3.png")
plt.close()


#############
# EJERCICIO 4
#############
# Read datasets
concern_polls = pd.read_csv("./data/concern_polls.csv")
pollsters = pd.read_excel("./data/pollster_ratings.xlsx", index_col=0)
# Processing grades
concern_polls_grades = utils.grade_cleaning(concern_polls, pollsters)

##### Ej 4.1 #####
total_people = concern_polls_grades.sample_size.sum()
print("A total of {} people has been interviewed".format(total_people))

##### Ej 4.2 #####
# Filter by economy
concern_polls_economy = utils.pattern_search("economy", concern_polls_grades, "subject")
# Group sum
very = sum(concern_polls_economy.very * concern_polls_economy.sample_size / 100)
somewhat = sum(concern_polls_economy.somewhat * concern_polls_economy.sample_size / 100)
not_very = sum(concern_polls_economy.not_very * concern_polls_economy.sample_size / 100)
not_at_all = sum(concern_polls_economy.not_at_all * concern_polls_economy.sample_size / 100)
# Plot args
height = [very, somewhat, not_very, not_at_all]
bars = ("very", "somewhat", "not_very", "not_at_all")
ticks = list(range(len(bars)))
# Bar Plot
plt.bar(ticks, height)
plt.title("economy concern")
plt.ylabel("Counts")
plt.xticks(ticks, bars)
plt.savefig("./figures/Ejercicio4_2.png")
plt.close()

##### Ej 4.3 #####
# Filter by infected
concern_polls_infected = utils.pattern_search("infected", concern_polls_grades, "subject")
# Group sum
total_people_infected = concern_polls_infected.sample_size.sum()
very = sum(concern_polls_infected.very * concern_polls_infected.sample_size / 100)
somewhat = sum(concern_polls_infected.somewhat * concern_polls_infected.sample_size / 100)
not_very = sum(concern_polls_infected.not_very * concern_polls_infected.sample_size / 100)
not_at_all = sum(concern_polls_infected.not_at_all * concern_polls_infected.sample_size / 100)
# Percentages
very_per = very / total_people_infected * 100
somewhat_per = somewhat / total_people_infected * 100
not_very_per = not_very / total_people_infected * 100
not_at_all_per = not_at_all / total_people_infected * 100
# Plot args
height = [very_per, somewhat_per, not_very_per, not_at_all_per]
bars = ("very", "somewhat", "not_very", "not_at_all")
ticks = list(range(len(bars)))
# Bar Plot
plt.bar(ticks, height)
plt.title("infected concern")
plt.ylabel("Counts %")
plt.xticks(ticks, bars)
plt.savefig("./figures/Ejercicio4_3.png")
plt.close()

##### Ej 4.4 #####
# Group by grades
interviews_by_grade = concern_polls_grades.groupby("538 Grade")
interviews_by_grade = interviews_by_grade.count().iloc[:, 0]
# Plot
interviews_by_grade.plot(kind="bar")
plt.title("Interviews by grade")
plt.ylabel("Count"); plt.xlabel("Grade")
plt.savefig("./figures/Ejercicio4_4.png")
plt.close()


#############
# EJERCICIO 5
#############
# Read dataset
concern_polls_grades = pd.read_csv("./data/concern_polls_grades.csv")
# Puntuation column
concern_polls_grades["puntation"] = concern_polls_grades["538 Grade"].map(utils.grades_to_number) + \
                                    concern_polls_grades["Predictive    Plus-Minus"]
##### Ej 5.1 #####
# Filtro
concern_polls_best_grades = concern_polls_grades[concern_polls_grades["puntation"] >= 1.5].copy()
#To Date
concern_polls_best_grades.loc[:, "end_date"] = pd.to_datetime(concern_polls_best_grades["end_date"])
# Date frontier
date_limit = pd.to_datetime("2020-09-01")
concern_polls_best_grades.loc[:, "date_limit"] = concern_polls_best_grades["end_date"].apply(
    lambda x: 1 if x > date_limit else 0)

##### Ej 5.1 A #####
# Total
concern_polls_best_grades.loc[:, ["very", "somewhat", "not_very", "not_at_all"]] = \
        concern_polls_best_grades[["very", "somewhat", "not_very", "not_at_all"]].multiply(
        concern_polls_best_grades["sample_size"], axis="index") / 100
# Groupby
bestGradesByDate = concern_polls_best_grades.groupby(by="date_limit")
Total = bestGradesByDate.sum()[["very", "somewhat", "not_very", "not_at_all"]]
# Plot
Total.plot(kind="bar")
plt.title("Concern by date")
plt.ylabel("Count"); plt.xlabel("Date")
plt.savefig("./figures/Ejercicio5_1A.png")
plt.close()

##### Ej 5.1 B #####
# Percentage
Perc = Total.div(bestGradesByDate.sum()["sample_size"], axis = "index")*100
# Plot
Perc.plot(kind="bar")
plt.title("Concern by date")
plt.ylabel("Percentage"); plt.xlabel("Date")
plt.savefig("./figures/Ejercicio5_1B.png")

##### Ej 5.2 #####
# Pasado el 1 de Setiembre la la cantidad de gente concienciada es mayor
# simplemente porque la cantidad de gente entrevisada ha aumentado. La realidad es
# completamente lo contrario. El porcentaje de gente concienciada ante la epidemia ha dismimuido.