import pandas as pd

def calculate_usage(sales_df, recipe_df):
    usage = []

    for _, s in sales_df.iterrows():
        recipe = recipe_df[recipe_df['menu'] == s['menu']]

        for _, r in recipe.iterrows():
            usage.append({
                "produk": r['bahan'],
                "qty": r['qty'] * int(s['qty'])
            })

    return pd.DataFrame(usage)

def calculate_stock(trans_df, sales_df, recipe_df):
    trans_df['qty'] = trans_df['qty'].astype(int)

    stock_in = trans_df[trans_df['tipe']=="IN"].groupby('produk')['qty'].sum()
    stock_out_manual = trans_df[trans_df['tipe']=="OUT"].groupby('produk')['qty'].sum()

    usage_df = calculate_usage(sales_df, recipe_df)
    stock_out_sales = usage_df.groupby('produk')['qty'].sum()

    stock = pd.DataFrame({
        "IN": stock_in,
        "OUT_manual": stock_out_manual,
        "OUT_sales": stock_out_sales
    }).fillna(0)

    stock["stok"] = stock["IN"] - stock["OUT_manual"] - stock["OUT_sales"]

    return stock.reset_index()
