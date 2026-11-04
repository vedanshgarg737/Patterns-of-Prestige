#import "@preview/metropole-report:0.1.0": *

#show: metropole.with(
  title: "An Analysis of India's Civilian and Military Honours",
  subtitle: "Team 007"
)
#show link: underline

#set heading(numbering: "1.1.")
#outline()

#pagebreak()

= Meta Information

This report is in relation to the open project titled *An Analysis of India's Civilian and Military Honours* by *Team 007* under the guidance of mentor _Mayank Jain_ (25B1024).

The members of the team are as follows.
+ Vedansh Garg - 25B0950
+ Akshita Jain - 25B0999
+ Maulik - 25B1002
+ Arush Anand - 25B1012

== Honour Code

We did not engange with any help (human) outside of our group and mentor for the duration of the project. AI assistance used during the project is disclosed further into the report.

== LLM Use Disclosure

+ #link("https://share.gemini.google/wDSPNs8JMhfm")[Topic Brainstorming]
+ #link("https://claude.ai/share/5dfc40cd-7429-4f5a-b609-8dd7ba3c48e5")[LaTeX formatting]
+ #link("https://claude.ai/share/70d6baf3-571b-4629-b569-b21df0c9ae42")[Bash Script Generation]
+ #link("https://claude.ai/share/db44445b-69e5-4c4c-b2ce-462f125d4133")[Pie chart formatting]
+ #link("https://claude.ai/share/9607aaef-c5a8-4fda-b6a3-868d8eddbc16")[Conclusion outlining]
+ #link("https://share.gemini.google/KS46bRYG1z1p")[Processing Data]
+ #link("https://claude.ai/share/35a5cbd9-038c-4478-8096-b2c29a41c99c")[Approach outlining]


== Video Presentation

#link("https://drive.google.com/file/d/10G1O2w6m_Zq-gznUWVOona-b9vlFcZD6/view?usp=sharing")[Project Description Video]

== Github Repository Link

+ #link("https://github.com/vedanshgarg737/DAI_PROJECT_007.git")[Personal repository]
+ #link("https://github.com/cs215-cse-iitb/dai-aug-2026-openproject-group-7.git")[Organisation repository]

The personal repository is a branch of the organisaiton repository.

#pagebreak()
== Github Contributions

#table(
  columns: (auto, auto),
  inset: 10pt,
  align: horizon,
  table.header(
    [*Handle*], [*Work history*],
  ),
  [#link("https://github.com/vedanshgarg737")[vedanshgarg737]],
  [Worked on research statements and submissions with first commit on 2nd November, 2026],
  [#link("https://github.com/akshitajain1528")[akshitajain1528]],
  [Worked on proposal and checkpoint reports with first commit on 1st November, 2026],
  [#link("https://github.com/MaulikJain07")[MaulikJain07]],
  [Worked on the coding part and repository initialization with first commit on 12th October, 2026],
  [#link("https://github.com/arushisboolied")[arushisboolied]],
  [Worked on the coding part and repository management with first commit on 20th October, 2026]
)

== Contribution Breakdown

#table(
  columns: (auto, auto),
  inset: 10pt,
  align: horizon,
  table.header(
    [*Member*], [*Contribution*],
  ),
  [Vedansh Garg],
  [Worked on the 1st Project Question, Dataset Collection and Project Submisisons - 100%],
  [Akshita Jain],
  [Worked on the 2nd Project Question, Processing of Datasets, Project Proposal, Checkpoint One Report and Final Presentation - 100%],
  [Maulik],
  [Worked on the 4th Project Question, Processing of Datasets and Repository Initialization and Video Presentation - 100%],
  [Arush Anand],
  [Worked on the 3rd Project Question, Cleaning of Datasets, Repository Management and Report - 100%],
  [LLMs],
  [Assisted with the code writing and processing of datasets via web scraping and Final Report - 125%]
)

#pagebreak()

= Core Problem Statement

== Broad Statement

This project analyzes India's civilian and military honours to determine how demographic, geographic, and age distributions have evolved over time. It compares civilian award trends (Bharat Ratna, Padma awards) with top gallantry awards (Ashoka Chakra, Param Vir Chakra) across four focus areas: regional/age shifts, gallantry vs. civilian demographics, category mix changes, and women's representation.

== Fine Grained Statements

#table(
  columns: (auto, auto, auto),
  inset: 3pt,
  align: horizon,
  table.header(
    [],[*Refined Question*],[*Hypotheses*]
  ),
  [Q1],[How have civilian winners changed in terms of region
  and age distribution between the first four decades and
  the latest four decades?],[H0: Region distribution and age distribution have remained the same. \
  H1: Region distribution has changed but the age
  distribution has remained the same. \
  H2: Region distribution has not changed but the age
  distribution has changed. \
  H3: Region distribution and age distribution have both
  changed.],
  [Q2],[How do gallantry winners compare with civilian winners
  in age, and how common are posthumous (after-death)
  awards?],[H0: No difference in age and gallantry awards are not
  more often posthumous. \
  H1: Gallantry winners are younger than civilian winners
  but gallantry awards are not often posthumous. \
  H3: Gallantry winners are younger than civilian winners,
  and gallantry awards are usually given after death.],
  [Q3],[Has the mix of civilian award categories shifted across
  decades?],[H0: The category mix is unchanged. \
  H1: The category mix has shifted.],
  [Q4],[Have women found increased representation in civilian
  awards across all fields?],[H0: Representation of women has not changed at all. \
  H1: Representation of women has increased but it is
  concentrated within a select few fields. \
  H2: Representation of women diversified but not
  increased in magnitude across all fields. \
  H3: Representation of women increased in magnitude
  across all fields and diversified as well.],
)

= Data Sources

#table(
  columns: (auto, auto, auto),
  inset: 10pt,
  align: horizon,
  table.header(
    [*File*], [*Contents*], [*Source*]
  ),
  [nationalawards.csv], [Bharat Ratna and Padma award recipients], [#link("https://www.kaggle.com/code/mohandeep20/padma-awards-1954-2021/input?select=padmaawards.csv")[Kaggle]],
  [ashokachakra.csv], [Ashoka Chakra recipients, the highest peacetime gallantry award], [#link("https://www.kaggle.com/code/mpwolke/ashokachakra-indian-gallantry-awards/notebook")[Kaggle], #link("https://www.gallantryawards.gov.in/")[Gallantry Awards portal]],
  [paramvirchakrarecipients.csv], [Param Vir Chakra recipients, the highest wartime gallantry award], [#link("https://www.gallantryawards.gov.in/")[Gallantry Awards Portal]],
)

= Tools and Software

#table(
  columns: (auto, auto),
  inset: 10pt,
  align: horizon,
  table.header(
    [*Purpose*], [*Tool*]
  ),
  [Data Handling], [Pandas],
  [Statistics], [Scipy.stats],
  [Visualisation], [Matplotlib, Seaborn],
  [Notebooks], [Jupyter],
  [Version Control], [Git, Github]
)


= Challenges and Results Achieved
== Challenges
+ Missing birth years. The datasets had no age information. We needed age for our questions, so we searched for the year of birth of every gallantry winner and added it ourselves.
+ Incomplete data. The Ashoka Chakra file had missing entries. We filled them in by hand and made a new cleaned file.
+ Same name, different spellings. One person appeared with different spellings. This would count them twice, so we fixed the names.
+ Very little data for gallantry awards. The Ashoka Chakra file has only 88 records and the Param Vir Chakra file has only 21. Because of this, we cannot make very strong claims from the results.
+ Old records were hard to complete. Many older civilian records had missing details. Finding birth years for all 4,876 civilian winners took a lot of time, so it took a lot of time and searches to find birth years and still some people's date of birth was not available on the internet so those could not be used for further calculations.
+ Cleaning files. Four of us were editing the same files. To avoid confusion, we wrote one cleaning function that everyone runs, and we shared it through GitHub.

== Results Achieved

We cleaned and standardised all three datasets: 4,876 civilian award records, 88 Ashoka Chakra records and 21 Param Vir Chakra records.
We built a reusable, version-controlled cleaning pipeline.
We narrowed our broad topic into four testable questions, each with a null hypothesis and alternative hypotheses.

== Key Findings

*Q1: Calculation rejected hypotheses H0, H1 and H2, the data supports hypothesis H3 - both region and age of the winners have seen a shift in distribution.*

#figure(
  image("./assets/awardAge.png", width: 80%),
  caption: [
    Age of awardees
  ],
)
#figure(
  image("./assets/region.png", width: 80%),
  caption: [
    Region the awardees are from
  ],
)
*Q2: Calculation rejected hypotheses H0, H1 and supported hypothesis H3 which states that Gallantry winners are younger as compared to civilian winners, and Gallantary awards are usually posthumous.*
#figure(
  image("./assets/ageCompare.png", width: 80%),
  caption: [
    Comparison between ages of awardees
  ],
)
#figure(
  image("./assets/postHumous.png", width: 80%),
  caption: [
    Share of posthumous winners
  ],
)
*Q3: Calculation rejected hypothesis H0 and the data supported hypothesis H1 which states that the category mix has shifted.*
#figure(
  image("./assets/representation.png", width: 80%),
  caption: [
    Distribution of fields
  ],
)
*Q4: Calculation rejected hypotheses H0 and H3, partly supported hypothesis H2 and best supported hypothesis H1 which states that women representation has increased but remains concentrated within a few fields.*
#figure(
  image("./assets/fieldShare.png", width: 80%),
  caption: [
    Women awardee's share by field
  ],
)
#figure(
  image("./assets/fieldCompare.png", width: 80%),
  caption: [
    Field share in women awardees
  ],
)

== Frequently Answered Questions (FAQ)

=== Q1. Where does your data come from, and how big is it?

We use three public datasets. nationalawards.csv has Bharat Ratna and Padma awards (4876 rows × 5 columns) from Kaggle. ashokachakra.csv has 88 rows × 5 columns, from Kaggle and the Gallantry Awards portal. param_vir_chakra_recipients.csv has 21 rows × 5 columns, from the Gallantry Awards portal of the Government of India. All three are open to everyone, so no permission was needed. We work in Python (Pandas, NumPy, scipy.stats) in Jupyter Notebooks, plot with Matplotlib, Seaborn and Plotly, and use Git and GitHub for version control.

=== Q2. Why did you pick the Ashoka Chakra and Param Vir Chakra and not other gallantry awards?

They are the highest peacetime and wartime gallantry awards, so together they let us compare both kinds of bravery, international and domestic, army and civillian, including how often awards are given after death. The downside is size: the Param Vir Chakra has only 21 recipients, so any conclusion from it has to be drawn carefully.

=== Q3. How much of your data was missing or messy, and how did you handle it?

Mostly the older records. Some entries had no year of birth, and the same person was sometimes spelled differently in different rows. We added year of birth for all Ashoka Chakra and Param Vir Chakra winners and for civilian winners from 1954 to 1960, filled in the missing Ashoka Chakra entries, and merged different spellings so each person appears once under one standard name. We also wrote a reusable cleaning function that we can re-run whenever the data changes.

=== Q4. Your first question was very broad. How did you narrow it down?

Our first question, how India has honoured service and sacrifice since independence, was too vague to test. After cleaning the data, we turned it into four specific questions on region and age of civilian winners, gallantry versus civilian winners, the mix of award categories, and representation of women. Each has a null hypothesis (H0) and alternatives (H1, H2, H3) that we can test.
