import pandas as pd
import plotnine as pn

if __name__ == "__main__":
    combined_data = pd.read_csv("kinship/outputs/combined_data.csv")
    df_normal = combined_data[combined_data['type'] != 'natural_check']
    df_natural_check = combined_data[combined_data['type'] == 'natural_check']
    combined_data = pd.read_csv("kinship/outputs/combined_data.csv")
    plot = (
        pn.ggplot(pn.aes(x="complexity", y="comm_cost"))
        + pn.geom_point(df_normal, pn.aes(color="type"))
        + pn.geom_point(df_natural_check, pn.aes(color="type"))
        + pn.geom_text(
            df_natural_check,
            pn.aes(label="name"),
            ha="left",
            size=6,
            nudge_x=1.5,
        )
    )
    plot.save("kinship/outputs/plot_slavic.png", width=8, height=6, dpi=300)
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
