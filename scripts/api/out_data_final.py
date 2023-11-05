from scripts.utilities.helper import *
from scripts.utilities.config import *


def type_of_delivery(s):
    if ((s['sender_outer_region'] == 'Miền Bắc') & (s['receiver_outer_region'] == 'Miền Nam')) \
            | ((s['sender_outer_region'] == 'Miền Nam') & (s['receiver_outer_region'] == 'Miền Bắc')):
        return 'Cách Miền'
    elif ((s['sender_outer_region'] == 'Miền Bắc') & (s['receiver_outer_region'] == 'Miền Trung')) \
            | ((s['sender_outer_region'] == 'Miền Trung') & (s['receiver_outer_region'] == 'Miền Nam')) \
            | ((s['sender_outer_region'] == 'Miền Trung') & (s['receiver_outer_region'] == 'Miền Bắc')) \
            | ((s['sender_outer_region'] == 'Miền Nam') & (s['receiver_outer_region'] == 'Miền Trung')):
        return 'Cận Miền'
    elif s['sender_province'] != s['receiver_province']:
        return 'Nội Miền'
    elif (s['receiver_inner_region'] == 'Nội Thành') \
            & (s['receiver_province'] in ['Thành phố Hồ Chí Minh', 'Thành phố Hà Nội']):
        return 'Nội Thành Tp.HCM - HN'
    elif (s['receiver_inner_region'] == 'Nội Thành') \
            & (s['receiver_province'] not in ['Thành phố Hồ Chí Minh', 'Thành phố Hà Nội']):
        return 'Nội Thành Tỉnh'
    elif (s['receiver_inner_region'] == 'Ngoại Thành') \
            & (s['receiver_province'] in ['Thành phố Hồ Chí Minh', 'Thành phố Hà Nội']):
        return 'Ngoại Thành Tp.HCM - HN'
    elif (s['receiver_inner_region'] == 'Ngoại Thành') \
            & (s['receiver_province'] not in ['Thành phố Hồ Chí Minh', 'Thành phố Hà Nội']):
        return 'Ngoại Thành Tỉnh'


def type_of_system_delivery(s):
    if (s['sender_province'] in ['Thành phố Hồ Chí Minh', 'Thành phố Hà Nội']) \
            & (s['sender_province'] == s['receiver_province']):
        return 1
    elif ((s['sender_province'] == 'Thành phố Hồ Chí Minh') & (
            s['receiver_province'] in ['Thành phố Hà Nội', 'Thành phố Đà Nẵng'])) \
            | ((s['sender_province'] == 'Thành phố Hà Nội') & (
            s['receiver_province'] in ['Thành phố Hồ Chí Minh', 'Thành phố Đà Nẵng'])) \
            | ((s['receiver_province'] == 'Thành phố Hồ Chí Minh') & (
            s['sender_province'] in ['Thành phố Hà Nội', 'Thành phố Đà Nẵng'])) \
            | ((s['receiver_province'] == 'Thành phố Hà Nội') & (
            s['sender_province'] in ['Thành phố Hồ Chí Minh', 'Thành phố Đà Nẵng'])):
        return 2
    elif ((s['sender_province'] == 'Thành phố Hồ Chí Minh') & (s['receiver_outer_region'] == 'Miền Nam')) \
            | ((s['sender_province'] == 'Thành phố Hà Nội') & (s['receiver_outer_region'] == 'Miền Bắc')) \
            | ((s['receiver_province'] == 'Thành phố Hồ Chí Minh') & (s['sender_outer_region'] == 'Miền Nam')) \
            | ((s['receiver_province'] == 'Thành phố Hà Nội') & (s['sender_outer_region'] == 'Miền Bắc')):
        return 3
    elif ((s['sender_province'] == 'Thành phố Hồ Chí Minh') & (
            s['receiver_outer_region'] in ['Miền Bắc', 'Miền Trung'])) \
            | (
            (s['sender_province'] == 'Thành phố Hà Nội') & (s['receiver_outer_region'] in ['Miền Trung', 'Miền Nam'])) \
            | ((s['receiver_province'] == 'Thành phố Hồ Chí Minh') & (
            s['sender_outer_region'] in ['Miền Bắc', 'Miền Trung'])) \
            | (
            (s['receiver_province'] == 'Thành phố Hà Nội') & (s['sender_outer_region'] in ['Miền Trung', 'Miền Nam'])):
        return 4
    elif s['sender_province'] == s['receiver_province']:
        return 5
    elif s['sender_outer_region'] == s['receiver_outer_region']:
        return 6
    elif ((s['sender_outer_region'] == 'Miền Bắc') & (s['receiver_outer_region'] in ['Miền Trung', 'Miền Nam'])) \
            | ((s['sender_outer_region'] == 'Miền Trung') & (s['receiver_outer_region'] in ['Miền Bắc', 'Miền Nam'])) \
            | ((s['sender_outer_region'] == 'Miền Nam') & (s['receiver_outer_region'] in ['Miền Bắc', 'Miền Trung'])) \
            | ((s['receiver_outer_region'] == 'Miền Bắc') & (s['sender_outer_region'] in ['Miền Trung', 'Miền Nam'])) \
            | ((s['receiver_outer_region'] == 'Miền Trung') & (s['sender_outer_region'] in ['Miền Bắc', 'Miền Nam'])) \
            | ((s['receiver_outer_region'] == 'Miền Nam') & (s['sender_outer_region'] in ['Miền Bắc', 'Miền Trung'])):
        return 7


def generate_sample_input(n_rows=1000):
    result_df = pd.DataFrame()
    result_df['order_id'] = [
        ''.join(np.random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 12)) \
        + ''.join(np.random.choice(list('123456789'), 9))
        for i in range(n_rows)
    ]
    result_df['sender_district_id'] = np.random.choice(PROVINCE_MAPPING_DISTRICT_DF['district_id'].tolist(), n_rows)
    result_df['receiver_district_id'] = np.random.choice(PROVINCE_MAPPING_DISTRICT_DF['district_id'].tolist(), n_rows)
    result_df = (
        result_df.merge(
            PROVINCE_MAPPING_DISTRICT_DF[['province_id', 'district_id']].rename(columns={
                'province_id': 'sender_province_id',
                'district_id': 'sender_district_id'
            }), on='sender_district_id', how='left')
            .merge(
            PROVINCE_MAPPING_DISTRICT_DF[['province_id', 'district_id']].rename(columns={
                'province_id': 'receiver_province_id',
                'district_id': 'receiver_district_id'
            }), on='receiver_district_id', how='left')
    )
    result_df['weight'] = [
        np.random.choice(list(range(100, 50000, 100)))
        for i in range(n_rows)
    ]

    result_df['delivery_type'] = [
        np.random.choice(['Lấy Tận Nơi', 'Gửi Bưu Cục'])
        for i in range(n_rows)
    ]

    return result_df[[
        'order_id', 'weight', 'delivery_type',
        'sender_province_id', 'sender_district_id', 'receiver_province_id', 'receiver_district_id',
    ]]


def generate_order_type(input_df):
    result_df = input_df.merge(pd.DataFrame(data={'carrier': ACTIVE_CARRIER}), how='cross')
    result_df['carrier_id'] = result_df['carrier'].map(MAPPING_CARRIER_ID)
    result_df = (
        result_df
            .merge(
            PROVINCE_MAPPING_DISTRICT_DF.rename(columns={
                'province_id': 'sender_province_id',
                'district_id': 'sender_district_id',
                'province': 'sender_province',
                'district': 'sender_district'
            }), on=['sender_province_id', 'sender_district_id'], how='left')
            .merge(
            PROVINCE_MAPPING_DISTRICT_DF.rename(columns={
                'province_id': 'receiver_province_id',
                'district_id': 'receiver_district_id',
                'province': 'receiver_province',
                'district': 'receiver_district'
            }), on=['receiver_province_id', 'receiver_district_id'], how='left')
    )

    phan_vung_nvc = pd.read_parquet(ROOT_PATH + '/processed_data/phan_vung_nvc.parquet')
    result_df = (
        result_df.merge(
            phan_vung_nvc.rename(columns={
                'receiver_province': 'sender_province',
                'receiver_district': 'sender_district',
                'outer_region': 'sender_outer_region',
                'inner_region': 'sender_inner_region',
            }), on=['carrier', 'sender_province', 'sender_district'], how='left').merge(
            phan_vung_nvc.rename(columns={
                'outer_region': 'receiver_outer_region',
                'inner_region': 'receiver_inner_region',
            }), on=['carrier', 'receiver_province', 'receiver_district'], how='left')
    )
    result_df['order_type'] = result_df.apply(type_of_delivery, axis=1)
    result_df['order_type_id'] = result_df['order_type'].map(MAPPING_ORDER_TYPE_ID)
    result_df['sys_order_type_id'] = result_df.apply(type_of_system_delivery, axis=1)

    return result_df.drop([
        'sender_outer_region', 'sender_inner_region',
        'receiver_outer_region', 'receiver_inner_region'
    ], axis=1)


def combine_info_from_api(input_df):
    api_data_final = pd.read_parquet('./output/data_api.parquet')
    result_df = (
        input_df.merge(
            api_data_final[[
                'receiver_province_id', 'receiver_district_id', 'carrier_id', 'order_type_id',
                'carrier_status', 'estimate_delivery_time_details', 'estimate_delivery_time',
                'customer_best_carrier', 'delivery_success_rate', 'score', 'stars', 'total_order',
            ]], on=['receiver_province_id', 'receiver_district_id', 'carrier_id', 'order_type_id'], how='left'
        )
    )
    return result_df


def calculate_service_fee(input_df):
    cuoc_phi_df = pd.read_parquet('./processed_data/cuoc_phi.parquet')
    cuoc_phi_df = cuoc_phi_df[['carrier', 'order_type', 'gt', 'lt_or_eq', 'service_fee']]

    # 3. Tổng hợp
    result_df = input_df.merge(cuoc_phi_df, on=['carrier', 'order_type'], how='inner')
    result_df = result_df.loc[
        (result_df['weight'] > result_df['gt']) &
        (result_df['weight'] <= result_df['lt_or_eq'])
        ]

    # Ninja Van lấy tận nơi cộng cước phí 1,500
    result_df.loc[
        result_df['carrier'].isin(['Ninja Van']) &
        result_df['delivery_type'].isin(['Lấy Tận Nơi']),
        'service_fee'
    ] = result_df['service_fee'] + 1500

    # GHN lấy tận nơi cộng cước phí 1,000
    result_df.loc[
        result_df['carrier'].isin(['GHN']) &
        result_df['delivery_type'].isin(['Lấy Tận Nơi']),
        'service_fee'
    ] = result_df['service_fee'] + 1000

    return result_df.drop(['gt', 'lt_or_eq'], axis=1)


def calculate_notification(input_df):
    re_nhat_df = input_df.groupby(['order_id'])['service_fee'].min().reset_index()
    re_nhat_df['notification'] = 'Rẻ nhất'
    # Gắn ngược lại để lấy đủ row (trong trường hợp có nhiều carrier cùng mức giá
    re_nhat_df = re_nhat_df.merge(input_df, on=['order_id', 'service_fee'], how='inner')

    remain_df1 = merge_left_only(input_df, re_nhat_df, keys=['order_id', 'service_fee'])

    nhanh_nhat_df = remain_df1.groupby(['order_id'])['estimate_delivery_time_details'].min().reset_index()
    nhanh_nhat_df['notification'] = 'Nhanh nhất'
    nhanh_nhat_df = nhanh_nhat_df.merge(remain_df1, on=['order_id', 'estimate_delivery_time_details'],
                                        how='inner')

    remain_df2 = merge_left_only(remain_df1, nhanh_nhat_df,
                                 keys=['order_id', 'estimate_delivery_time_details'])

    hieu_qua_nhat_df = remain_df2.groupby(['order_id'])['score'].max().reset_index()
    hieu_qua_nhat_df['notification'] = 'Dịch vụ tốt'
    hieu_qua_nhat_df = hieu_qua_nhat_df.merge(remain_df2, on=['order_id', 'score'], how='inner')

    remain_df3 = merge_left_only(remain_df2, hieu_qua_nhat_df, keys=['order_id', 'score'])
    remain_df3['notification'] = 'Bình thường'

    result_df = pd.concat([
        re_nhat_df,
        nhanh_nhat_df,
        hieu_qua_nhat_df,
        remain_df3
    ], ignore_index=True)


def partner_best_carrier(data_api_df, threshold=15):
    df1 = data_api_df.loc[data_api_df['total_order'] > threshold]
    df2 = data_api_df.loc[(data_api_df['total_order'] >= 1) & (data_api_df['total_order'] <= threshold)]
    df3 = data_api_df.loc[data_api_df['total_order'] == 0]

    group1 = (
        df1.sort_values(['service_fee', 'delivery_success_rate'], ascending=[False, False])
            .drop_duplicates(['receiver_province', 'receiver_district', 'order_type'], keep='first')
        [['receiver_province', 'receiver_district', 'order_type', 'carrier']]
            .rename(columns={'carrier': 'partner_best_carrier'})
    )
    group2 = (
        df2.sort_values(['delivery_success_rate', 'service_fee'], ascending=[False, False])
            .drop_duplicates(['receiver_province', 'receiver_district', 'order_type'], keep='first')
        [['receiver_province', 'receiver_district', 'order_type', 'carrier']]
            .rename(columns={'carrier': 'partner_best_carrier'})
    )
    group3 = df3[['receiver_province', 'receiver_district', 'order_type']].drop_duplicates()
    group3['partner_best_carrier'] = PARTNER_BEST_CARRIER_DEFAULT

    partner_best_carrier_df = pd.concat([group1, group2, group3]).drop_duplicates(
        ['receiver_province', 'receiver_district', 'order_type'], keep='first')

    return partner_best_carrier_df


def out_data_final(generate_sample=False):
    if generate_sample:
        input_df = generate_sample_input(n_rows=10_000)
    else:
        giao_dich_valid = pd.read.parquet('./processed_data/giao_dich_combine_valid.parquet')
        giao_dich_valid = giao_dich_valid[[
            'order_id', 'weight', 'delivery_type', 'sender_province', 'sender_district',
            'receiver_district', 'receiver_district'
        ]]
        input_df = (
            giao_dich_valid.merge(
                PROVINCE_MAPPING_DISTRICT_DF.rename(columns={
                    'province_id': 'sender_province_id',
                    'district_id': 'sender_district_id',
                    'province': 'sender_province',
                    'district': 'sender_district'
                }), on=['sender_province', 'sender_district'], how='left')
                .merge(
                PROVINCE_MAPPING_DISTRICT_DF.rename(columns={
                    'province_id': 'receiver_province_id',
                    'district_id': 'receiver_district_id',
                    'province': 'receiver_province',
                    'district': 'receiver_district'
                }), on=['receiver_province_id', 'receiver_district_id'], how='left')
        )
        input_df = input_df[[
            'order_id', 'weight', 'delivery_type', 'sender_province_id', 'sender_district_id',
            'receiver_district_id', 'receiver_district_id'
        ]]
        assert len(giao_dich_valid) == len(input_df), 'Transform data sai'

    tmp_df1 = generate_order_type(input_df)
    assert len(tmp_df1) == len(input_df) * len(ACTIVE_CARRIER), 'Transform data sai'

    tmp_df2 = combine_info_from_api(tmp_df1)
    assert len(tmp_df2) == len(tmp_df1), 'Transform data sai'

    tmp_df3 = calculate_service_fee(tmp_df2)
    assert len(tmp_df3) == len(tmp_df2), 'Transform data sai'

    tmp_df4 = calculate_notification(tmp_df3)
    assert len(tmp_df4) == len(tmp_df3), 'Transform data sai'

    partner_best_carrier_df = partner_best_carrier(tmp_df4)

    final_df = (
        tmp_df4.merge(
            partner_best_carrier_df,
            on=['receiver_province', 'receiver_district', 'order_type'],
            how='inner'
        )
    )
    assert len(final_df) == len(tmp_df4), 'Transform data sai'

    final_df = final_df[[
        'order_id',
        'sender_province_id', 'sender_province', 'sender_district_id', 'sender_district',
        'receiver_province_id', 'receiver_province', 'receiver_district_id', 'receiver_district',
        'carrier_id', 'carrier', 'order_type', 'order_type_id', 'sys_order_type_id',
        'weight', 'service_fee', 'delivery_type',
        'carrier_status', 'estimate_delivery_time_details', 'estimate_delivery_time', 'delivery_success_rate',
        'customer_best_carrier', 'partner_best_carrier', 'score', 'stars', 'notification',
    ]]

    if generate_sample:
        return final_df
    else:
        final_df.to_parquet('./output/data_final.parquet')
        # print('Lưu dữ liệu respone request')
        # with open('./output/data_final_respone_request.json', 'w', encoding='utf-8') as file:
        #     final_df.to_json(file, force_ascii=False)

    print('>>> Done\n')
    print('-' * 100)


if __name__ == '__main__':
    out_data_final()