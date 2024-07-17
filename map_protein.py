import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import pandas as pd
st.set_page_config(layout="wide")
from streamlit_agraph.config import Config, ConfigBuilder

#getting data
final_vd = pd.read_csv(r'./final_top51.csv')
#setting sidebar
type_n = final_vd['node_type'].unique()
type_c = final_vd['Condition'].unique()
with st.sidebar:
    category = st.selectbox(
        'Please select your category:',
        type_n)

if category:
    with st.sidebar:
        option = st.selectbox(
        'Please select your Type:',
        type_c)

    st.bar_chart(pd.DataFrame(final_vd['Condition'].value_counts(), x="Condition", y="Disease_count"))
    
    #getting data for KG
    final_arr_short = final_vd[final_vd.Condition == option]
     
    #initializing buckets
    nodes = []
    edges = []
     
    df_genes = dict()
     
    st.title('Knowledge Graph')
    df_genes=dict(enumerate(final_arr_short.Protein.unique()))
    for i in df_genes:
                nodes.append( Node(id=df_genes[i],
                            label=df_genes[i],
                            size=25,
                            shape="diamond",
                            color='#00008B'
                            )
                        ) # includes **kwargs
     
    df_disease = pd.DataFrame(final_arr_short.neighbour_name.value_counts().reset_index().values, columns=["name", "count"])
    df_disease = df_disease.sort_index(axis = 0, ascending=True)
    df_disease = df_disease[df_disease.name != 'na']
    for index, row in df_disease.iterrows():
                nodes.append( Node(id=row['name'],
                            label=row['name'],
                            size=10 * row['count'],
                            shape="square",
                            color='#bf9b30'
                            )
                        ) # includes **kwargs
     
    df_condition = dict()
    df_condition=dict(enumerate(final_arr_short.Condition.unique()))
    for k in df_condition:
                nodes.append(Node(id=df_condition[k],
                            label=f"          {option}          ",
                            size=200,
                            shape="circle",
                            color='#00FFFF'
                            )
                        ) # includes **kwargs
     
    df_connections = final_arr_short.filter(items=['Protein', 'neighbour_name']).drop_duplicates()
    df_connections = df_connections[df_connections.neighbour_name != 'na']
    for index, row in df_connections.iterrows():          
            edges.append(Edge(source=row['Protein'],
                            label="--",
                            target=row['neighbour_name'],
                            # **kwargs
                            )
                        )
            
    df_mconnections = final_arr_short.filter(items=['Protein', 'Condition']).drop_duplicates()
    for index, row in df_mconnections.iterrows():        
            edges.append(Edge(source=row['Condition'],
                            label="--",
                            target=row['Protein'],
                            # **kwargs
                            )
                        )
    # 1. Build the config (with sidebar to play with options) .
    config_builder = ConfigBuilder(nodes)
    config = config_builder.build()
     
    # 2. If your done, save the config to a file.
    config.save("config.json")
     
    # 3. Simple reload from json file (you can bump the builder at this point.)
    config = Config(from_json="config.json")
     
    return_value = agraph(nodes=nodes,
                          edges=edges,
                          config=config)
