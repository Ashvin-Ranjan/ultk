import pandas as pd
import plotnine as pn

if __name__ == "__main__":
    combined_data = pd.read_csv("kinship/outputs/combined_data.csv")
    df_normal = combined_data[(combined_data['type'] != 'natural_check') & (combined_data['type'] != 'drift')]
    df_drift = combined_data[combined_data['type'] == 'drift']
    df_natural_check = combined_data[combined_data['type'] == 'natural_check']
    combined_data = pd.read_csv("kinship/outputs/combined_data.csv")
    with open("kinship/data/langs_english_chains.txt", 'r') as f:
        chains = [l.split(" -> ") for l in f.read().split("\n")]
    chains_data = {"x": [], "y": [], "endy": [], "endx": []}
    for chain in chains:
        start = df_natural_check.loc[df_natural_check['name'] == chain[0]]
        end = df_natural_check.loc[df_natural_check['name'] == chain[1]]
        
        if not start.empty and not end.empty:
            chains_data["x"].append(start["complexity"].values[0])
            chains_data["y"].append(start["comm_cost"].values[0])
            chains_data["endx"].append(end["complexity"].values[0])
            chains_data["endy"].append(end["comm_cost"].values[0])

    df_chains = pd.DataFrame(chains_data)
    
    plot = (
        pn.ggplot()
        + pn.geom_point(df_normal, pn.aes(x="complexity", y="comm_cost", color="type"))
        + pn.geom_point(df_drift, pn.aes(x="complexity", y="comm_cost", color="type"))
        + pn.geom_point(df_natural_check, pn.aes(x="complexity", y="comm_cost", color="type"))
        + pn.geom_segment(df_chains, pn.aes(x="x", y="y", yend="endy", xend="endx"), arrow=pn.arrow(length=0.02))
        # + pn.geom_text(
        #     df_natural_check,
        #     pn.aes(x="complexity", y="comm_cost", label="name"),
        #     ha="left",
        #     size=6,
        #     nudge_x=1.5,
        # )
    )
    plot.save("kinship/outputs/plot_english.png", width=8, height=6, dpi=300)
    # combined_data = pd.read_csv("kinship/outputs/combined_data.csv")
    # plot = (
    #     pn.ggplot(pn.aes(x="complexity", y="comm_cost"))
    #     + pn.geom_point(combined_data, pn.aes(color="type"))
    #     + pn.geom_text(
    #         combined_data[combined_data["type"] == "natural_check"],
    #         pn.aes(label="name"),
    #         ha="left",
    #         size=6,
    #         nudge_x=0.5,
    #     )
    # )
    # plot.save("kinship/outputs/plot_text.png", width=8, height=6, dpi=300)
