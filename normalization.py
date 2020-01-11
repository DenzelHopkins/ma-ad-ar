import datetime


def normalization(df_features):
    # normalization of vector_array
    for column in df_features:
        if isinstance(df_features[column].max(), datetime.datetime):
            break
        else:
            if df_features[column].max() > 1:
                for index, x in df_features[column].items():
                    new_x = ((x - df_features[column].min()) / (df_features[column].max() - df_features[column].min()))
                    df_features[column][index] = new_x

    return df_features
