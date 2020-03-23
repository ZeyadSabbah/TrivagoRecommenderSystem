import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
import math
import matplotlib.pyplot as plt
from datetime import datetime

class data_transformation:
        def transform_data(data):
            def get_data_clickout(data):
              data_clickout = data[data['action_type']=='clickout item'].groupby('session_id').tail(1)
              return data_clickout

            def get_item_id(data_clickout):
              item_id = data_clickout[['session_id', 'impressions']]
              item_id['impressions'] = item_id['impressions'].apply(lambda x: x.split('|'))
              item_id = item_id.explode('impressions')
              item_id = item_id.rename(columns={'impressions':'item_id'})
              item_id = item_id.reset_index(drop=True)
              return item_id
              
            def get_clickout(data_clickout, data, item_id):
              clickout = data_clickout[['session_id','reference']]
              clickout = item_id.merge(clickout, on='session_id', how='left')
              clickout['clickout'] = clickout.apply(lambda x: 1 if x['item_id'] == x['reference'] else 0, axis=1)
              clickout.drop(columns='reference', inplace=True)
              clickout = clickout.reset_index(drop=True)
              IndexToNan = data_clickout.reference.index.values.tolist()
              data.loc[IndexToNan, 'reference'] = np.nan
              return clickout, data

            def get_price(data_clickout):
              price = data_clickout[['session_id', 'prices']]
              price['prices'] = price['prices'].apply(lambda x: x.split('|'))
              price = price.explode('prices')
              price['prices'] = price['prices'].apply(lambda x: int(x))
              price = price.rename(columns={'prices':'price'})
              price = price.reset_index(drop=True)
              return price

            def get_item_rank(data_clickout):
              item_rank = data_clickout[['session_id', 'impressions']]
              item_rank['impressions'] = item_rank['impressions'].apply(lambda x: x.split('|'))
              item_rank['impressions'] = item_rank['impressions'].apply(lambda x: list(range(1, len(x) + 1)))
              item_rank = item_rank.explode('impressions')
              item_rank = item_rank.rename(columns={'impressions':'item_rank'})
              item_rank = item_rank.reset_index(drop=True)
              return item_rank

            def get_price_rank(data):
              price_rank = data.groupby('session_id', sort=False).price.apply(lambda x: x.values).to_frame().reset_index().rename(columns={'price':'price_list'})
              price_rank.price_list = price_rank.price_list.apply(lambda x: np.argsort(x))
              price_rank = price_rank.rename(columns={'price_list':'price_rank'})
              price_rank = price_rank.explode('price_rank')
              price_rank = price_rank.reset_index(drop=True)
              return price_rank

            def get_session_duration(data, item_id):
              session_duration = data.groupby('session_id', sort=False).timestamp.max() - data.groupby('session_id', sort=False).timestamp.min()
              session_duration = session_duration.to_frame().rename(columns={'timestamp':'session_duration'})
              session_duration = item_id.merge(session_duration, on='session_id', how='left')
              session_duration.drop(columns='item_id', inplace=True)
              session_duration = session_duration.reset_index(drop=True)
              return session_duration

            def get_item_duration(data, item_id):
              item_duration = data.groupby(['session_id', 'reference'], sort=False).timestamp.max() - data.groupby(['session_id', 'reference'], sort=False).timestamp.min()
              item_duration = item_duration.reset_index().rename(columns={'reference':'item_id', 'timestamp':'item_duration'})
              item_duration = item_id.merge(item_duration, left_on=['session_id', 'item_id'], right_on=['session_id', 'item_id'], how='left')
              item_duration = item_duration.fillna(0)
              item_duration = item_duration.reset_index(drop=True)
              return item_duration

            def get_item_session_duration(item_duration, session_duration):
              item_duration['item_session_duration'] = item_duration.item_duration/session_duration.session_duration
              item_session_duration = item_duration[['session_id', 'item_id', 'item_session_duration']]
              item_duration = item_duration[['session_id', 'item_id', 'item_duration']]
              item_session_duration = item_session_duration.fillna(0)
              item_session_duration = item_session_duration.reset_index(drop=True)
              return item_session_duration

            def get_item_interactions(data, item_id):
              item_interactions = data.groupby(['session_id', 'reference']).step.count().to_frame().reset_index()
              item_interactions = item_interactions.rename(columns={'reference':'item_id', 'step':'item_interactions'})
              item_interactions = item_id.merge(item_interactions, left_on=['session_id', 'item_id'], right_on=['session_id', 'item_id'], how='left')
              item_interactions = item_interactions.fillna(0)
              item_interactions = item_interactions.reset_index(drop=True)
              return item_interactions

            def get_maximum_step(data, item_id):
              maximum_step = data.groupby('session_id', sort=False).step.max().to_frame().reset_index()
              maximum_step = maximum_step.rename(columns={'step':'maximum_step'})
              maximum_step = item_id.merge(maximum_step, on='session_id', how='left')
              maximum_step = maximum_step.reset_index(drop=True)
              return maximum_step

            def get_top_list(item_rank):
              top_list = item_rank[['session_id', 'item_rank']]
              top_list['top_list'] = top_list.apply(lambda x: 1 if x['item_rank'] < 6 else 0, axis=1)
              top_list = top_list.reset_index(drop=True)
              return top_list
              
            
            FinalClickoutDF = get_data_clickout(data)
            item_id = get_item_id(FinalClickoutDF)
            clickout, data = get_clickout(FinalClickoutDF, data, item_id)
            price = get_price(FinalClickoutDF)
            item_rank = get_item_rank(FinalClickoutDF)
            price_rank = get_price_rank(price)
            session_duration = get_session_duration(data, item_id)
            item_duration = get_item_duration(data, item_id)
            item_session_duration = get_item_session_duration(item_duration, session_duration)
            item_interactions = get_item_interactions(data, item_id)
            maximum_step = get_maximum_step(data, item_id)
            top_list = get_top_list(item_rank)

            local_data = item_id.copy()
            local_data['price'] = price.price
            local_data['item_rank'] = item_rank.item_rank
            local_data['price_rank'] = price_rank.price_rank
            local_data['clickout'] = clickout.clickout
            local_data['session_duration'] = session_duration.session_duration
            local_data['item_duration'] = item_duration.item_duration
            local_data['item_session_duration'] = item_session_duration.item_session_duration
            local_data['item_interactions'] = item_interactions.item_interactions
            local_data['maximum_step'] = maximum_step.maximum_step
            local_data['top_list'] = top_list.top_list
            GlobalPath = './Datasets/clean_data/ItemsFeatures/item_global.csv'
            GlobalData = pd.read_csv(GlobalPath)
            GlobalData.item_id = GlobalData.item_id.apply(lambda x: str(x))
            data = local_data.merge(GlobalData, on='item_id', how='left')
            NaNcolumns = ['NumberOfProperties', 'NumberInImpressions', 'NumberInReferences', 'NumberAsClickout', 'NumberAsFinalClickout',
                          'FClickoutToImpressions', 'FClickoutToReferences', 'FClickoutToClickout', 'MeanPrice', 'AveragePriceRank']
            for column in NaNcolumns:
              MeanValue = data[column].mean()
              data[column] =  data[column].fillna(MeanValue)
            data.item_id = data.item_id.apply(lambda x: str(x))

            return data
