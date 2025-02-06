import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style='white')

st.set_page_config(
  page_title="Dashboard Mapping Assist.id",
  page_icon="🗺️",
  layout="centered",
  initial_sidebar_state="collapsed",
)

@st.cache_data()
def load_data():
  mp_xl = pd.read_excel("./mp-2.xlsx", engine="openpyxl", sheet_name=None)
  return mp_xl

mp_xl = load_data()

st.title("🗺️Dashboard Mapping Assist.id")

def totalDoneByTeams():
  total_dones = []
  for name in mp_xl:
    total_dones.append(mp_xl[name]["match"].notna().sum())
  return total_dones

def totalDoneMapping():
  total_item = 0
  for name in mp_xl:
    filled = (mp_xl[name]["match"].notna() & 
      (mp_xl[name]["match"] != "")
    ).sum()
    data = len(mp_xl[name])
    if filled == data:
      total_item += 1
  return total_item

def totalUndoneMapping():
  total_item = 0
  for name in mp_xl:
    if mp_xl[name]["match"].notna().sum() != len(mp_xl[name]):
      total_item += 1
  return total_item

def totalItem():
  total_item = 0
  for name in mp_xl:
    total_item += len(mp_xl[name])
  return total_item

def totalMapped():
  total_item = 0
  for name in mp_xl:
    total_item += (mp_xl[name]["match"].notna() & 
      (mp_xl[name]["match"] != "")
    ).sum()
  return total_item

def totalUnmapped():
  total_item = 0
  for name in mp_xl:
    total_item += (mp_xl[name]["match"].isna() | 
      (mp_xl[name]["match"] == "")
    ).sum()
  return total_item

def totalMatched():
  total_item = 0
  for name in mp_xl:
    total_item += (mp_xl[name]["match"].notna() & 
      (mp_xl[name]["match"] != "") & 
      (mp_xl[name]["match"].str.lower() != "n")
    ).sum()
  return total_item

def totalRevision():
  total_item = 0
  for name in mp_xl:
    total_item += (
      mp_xl[name]["match"].notna() & 
      (mp_xl[name]["match"] != "") & 
      mp_xl[name]["revisi_nama"].notna() & 
      (mp_xl[name]["revisi_nama"] != "") & 
      (mp_xl[name]["revisi_nama"].str.lower() != "n")
        ).sum()
  return total_item

def totalHavePrincipal():
  total_item = 0
  for name in mp_xl:
    total_item += (
      mp_xl[name]["match"].notna() & 
      (mp_xl[name]["match"] != "") & 
      mp_xl[name]["revisi_nama"].notna() & 
      (mp_xl[name]["revisi_nama"] != "") & 
      mp_xl[name]["no_principal"].notna() & 
      (mp_xl[name]["no_principal"] != "") & 
      (mp_xl[name]["no_principal"].str.lower() == "n")
        ).sum()
  return total_item

def totalNoPrincipal():
  total_item = 0
  for name in mp_xl:
    total_item += (
      mp_xl[name]["match"].notna() & 
      (mp_xl[name]["match"] != "") & 
      mp_xl[name]["revisi_nama"].notna() & 
      (mp_xl[name]["revisi_nama"] != "") & 
      mp_xl[name]["no_principal"].notna() & 
      (mp_xl[name]["no_principal"] != "") & 
      (mp_xl[name]["no_principal"].str.lower() == "y")
        ).sum()
  return total_item



with st.container():
  st.subheader('🗒️Summary')

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    total_team = len(mp_xl.keys())
    st.metric("Team", value=total_team)
  with col2:
    total_item = totalItem()
    st.metric("Total Item", value=total_item)
  with col3:
    total_mapped = totalMapped()
    st.metric("Total Mapped", value=total_mapped)
  with col4:
    total_unmapped = totalUnmapped()
    st.metric("Total Unmapped", value=total_unmapped)

  col1, col2, col3, col4 = st.columns(4)

  with col1:
    total_matched = totalMatched()
    st.metric("Total Matched", value=total_matched)
  with col2:
    total_revision = totalRevision()
    st.metric("Total Revision", value=total_revision)
  with col3:
    total_haveprincipal = totalHavePrincipal()
    st.metric("Have Principal", value=total_haveprincipal)
  with col4:
    total_noprincipal = totalNoPrincipal()
    st.metric("No Principal", value=total_noprincipal)

  st.subheader('📊Graphics')

  data = {
    "Category": ["Mapped Match", "Revisi Match", "No Principal", "Have Principal"],
    "Count": [total_matched, total_revision, total_noprincipal, total_haveprincipal]
  }

  df = pd.DataFrame(data)

  colors = ["#CCECEC", "#FFCCCC", "#FFE8A1", "#C2E0FF"]

  fig, ax = plt.subplots(figsize=(8, 5))

  sns.barplot(data=df, hue="Category", x="Category", y="Count", palette=colors, edgecolor="black", ax=ax, legend=False)

  legend = ax.legend(["Details Mapped"], loc="upper center", bbox_to_anchor=(0.5, 1.05), frameon=True)
  legend.get_frame().set_linewidth(1)

  st.pyplot(fig)

  labels = ["Mapped", "Unmapped"]
  sizes = [total_mapped, total_unmapped]
  colors = ["#CCECEC", "#FFCCCC"]

  fig, ax = plt.subplots()

  ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=90, wedgeprops={"edgecolor": "black"})

  ax.set_title("Mapped vs Unmapped")

  st.pyplot(fig)

  st.subheader('👥Teams')

  col1, col2, col3 = st.columns(3)

  with col1:
    total_team = len(mp_xl.keys())
    st.metric("Total Team", value=total_team)
  with col2:
    total_done = totalDoneMapping()
    st.metric("Done Mapping", value=total_done)
  with col3:
    total_notdone = totalUndoneMapping()
    st.metric("Undone Mapping", value=total_notdone)

  data = {
    "Name": mp_xl.keys(),
    "Done": totalDoneByTeams()
  }

  df = pd.DataFrame(data)

  colors = ["#CCECEC", "#FFCCCC", "#FFE8A1", "#C2E0FF"]

  fig, ax = plt.subplots(figsize=(8, 5))

  sns.barplot(data=df, hue="Name", x="Name", y="Done", palette=colors, edgecolor="black", ax=ax, legend=False)
  plt.xticks(rotation=-90)

  legend = ax.legend(["Detail Teams"], loc="upper center", bbox_to_anchor=(0.5, 1.05), frameon=True)
  legend.get_frame().set_linewidth(1)

  st.pyplot(fig)


st.caption('Made with ❤️ by [ShadiqWP](https://github.com/uwoll)')