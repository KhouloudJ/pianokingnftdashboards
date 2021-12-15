import pandas as pd
import seaborn as sns
from etherscan import Etherscan
import streamlit as st
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')



def without_hue( plot, feature, title, criteria, x_axis_rotation=0, _format=None):
    sns.set(rc={'figure.figsize':(11.7,8.27)})
    plot.set_xticklabels(plot.get_xticklabels(), rotation=x_axis_rotation)
    for p in plot.patches:
        if p.get_height() > 0.01:
            if _format:
                final_p = "{:.2f}".format(p.get_height())
            else:
                final_p = p.get_height()
        x = p.get_x() + p.get_width() / 2 - 0.1
        y = p.get_y() + p.get_height() + 0.50
        plot.annotate(final_p, (x, y), size = 12)
        plot.set_title(title, fontsize=20, weight='bold')
        plot.set_xlabel(criteria, fontsize=14)
        plot.set_ylabel("Events Total", fontsize=14)
        plt.show()


def fmt(x):
    print(x)
    total = len(values)
    return '{:.4f}%\n({:.0f})'.format(x, total*x/100)



st.title('Piano king NFT Dashboards')
st.subheader('Distribution of events over 1,000 Piano King NFTs')
path_raw_data = "resources/output/pianoking_data.csv"
path_transac_history = "resources/output/transac_history_by_PK_NFT_ID.csv"
st.set_option('deprecation.showPyplotGlobalUse', False)

df = pd.read_csv(path_raw_data , sep=',')
# Import du csv en ométtant la première colonne d'index
df_transac_hist = pd.read_csv(path_transac_history, index_col=[0])
# Trick pour convertir la colonne Price en float64 (à convertir direct lors du scrap la prochaine fois)
df_transac_hist["Price"] = df_transac_hist["Price"].fillna(0)
df_transac_hist["Price"] = df_transac_hist["Price"].apply(lambda x : float(x.replace(",", ".")) if type(x) == str else x)
df_transac_hist["To"] = df_transac_hist["To"].apply(lambda x : str(x).replace("nan", ""))
df_transac_hist_grp = df_transac_hist.groupby(["TokenID", "Event"]).size().reset_index(name='Event_count')
df_transac_hist.groupby(["Event"]).size().reset_index(name='Event_count')

# dans la même journée la même offre au même montant pour éviter les mauvaises interprétations
df_transac_hist_nodup = df_transac_hist.drop_duplicates()

# Résultat avec la base sans les doublons
event_type_chart = sns.countplot(data=df_transac_hist_nodup, x="Event", palette="coolwarm")
without_hue(
    # "repartition_events_sans_doublons.png",
    event_type_chart, 
    df_transac_hist_nodup["Event"], 
    "Distribution of events over 1,000 Piano King NFTs", 
    "Event", 
    x_axis_rotation=0
)
st.pyplot()

values = pd.Series(df['FirstTimeOwner'])
v_counts = values.value_counts()
fig = plt.figure()
plt.pie(v_counts, labels=v_counts.index, autopct=fmt, shadow=False)
plt.show()
st.subheader('Piano King Primo Wallet Holders')
st.pyplot(fig)
