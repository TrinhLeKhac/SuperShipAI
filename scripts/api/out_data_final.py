import sys
from pathlib import Path

ROOT_PATH = str(Path(__file__).parent.parent.parent)
sys.path.append(ROOT_PATH)

from scripts.utilities.helper import *
from scripts.utilities.config import *
from scripts.api.out_data_api import out_data_api

API_FULL_COLS = [
    'order_code',
    'sender_province_code', 'sender_province', 'sender_district_code', 'sender_district',
    'receiver_province_code', 'receiver_province', 'receiver_district_code', 'receiver_district',
    'carrier_id', 'carrier', 'order_type', 'new_type', 'route_type',
    'weight', 'price', 'pickup_type',
    'status', 'description',
    'time_data', 'time_display',
    'rate', 'rate_ranking',
    'for_fshop', 'shop_best_carrier',
    'for_partner', 'partner_best_carrier', 'score', 'stars',
    'price_ranking', 'speed_ranking', 'score_ranking',
]
API_COLS = [
    'order_code', 'carrier_id', 'new_type', 'route_type', 'price',
    'status', 'description',
    'time_data', 'time_display', 'rate',
    'for_fshop', 'for_partner', 'score', 'stars',
    'price_ranking', 'speed_ranking', 'score_ranking',
]


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
    result_df['order_code'] = [
        ''.join(np.random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 12)) \
        + ''.join(np.random.choice(list('123456789'), 9))
        for i in range(n_rows)
    ]
    result_df['sender_district_code'] = np.random.choice(PROVINCE_MAPPING_DISTRICT_DF['district_code'].tolist(), n_rows)
    result_df['receiver_district_code'] = np.random.choice(PROVINCE_MAPPING_DISTRICT_DF['district_code'].tolist(), n_rows)
    result_df = (
        result_df.merge(
            PROVINCE_MAPPING_DISTRICT_DF[['province_code', 'district_code']].rename(columns={
                'province_code': 'sender_province_code',
                'district_code': 'sender_district_code'
            }), on='sender_district_code', how='left')
            .merge(
            PROVINCE_MAPPING_DISTRICT_DF[['province_code', 'district_code']].rename(columns={
                'province_code': 'receiver_province_code',
                'district_code': 'receiver_district_code'
            }), on='receiver_district_code', how='left')
    )
    result_df['weight'] = [
        np.random.choice(list(range(100, 50000, 100)))
        for i in range(n_rows)
    ]

    result_df['pickup_type'] = [
        np.random.choice(['Lấy Tận Nơi', 'Gửi Bưu Cục'])
        for i in range(n_rows)
    ]

    return result_df[[
        'order_code', 'weight', 'pickup_type',
        'sender_province_code', 'sender_district_code', 'receiver_province_code', 'receiver_district_code',
    ]]


def generate_order_type(input_df, carriers=ACTIVE_CARRIER):
    result_df = input_df.merge(pd.DataFrame(data={'carrier': carriers}), how='cross')
    result_df['carrier_id'] = result_df['carrier'].map(MAPPING_CARRIER_ID)
    result_df = (
        result_df
            .merge(
            PROVINCE_MAPPING_DISTRICT_DF.rename(columns={
                'province_code': 'sender_province_code',
                'district_code': 'sender_district_code',
                'province': 'sender_province',
                'district': 'sender_district'
            }), on=['sender_province_code', 'sender_district_code'], how='left')
            .merge(
            PROVINCE_MAPPING_DISTRICT_DF.rename(columns={
                'province_code': 'receiver_province_code',
                'district_code': 'receiver_district_code',
                'province': 'receiver_province',
                'district': 'receiver_district'
            }), on=['receiver_province_code', 'receiver_district_code'], how='left')
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
    result_df['new_type'] = result_df['order_type'].map(MAPPING_ORDER_TYPE_ID)
    result_df['route_type'] = result_df.apply(type_of_system_delivery, axis=1)

    return result_df.drop([
        'sender_outer_region', 'sender_inner_region',
        'receiver_outer_region', 'receiver_inner_region'
    ], axis=1)


def combine_info_from_api(input_df, show_logs=False):
    api_data_final = out_data_api(return_full_cols_df=True, show_logs=show_logs)
    result_df = (
        input_df.merge(
            api_data_final[[
                'receiver_province_code', 'receiver_district_code', 'carrier_id', 'new_type',
                'status', 'description',
                'time_data', 'time_display',
                'shop_best_carrier', 'for_fshop',
                'speed_ranking', 'score_ranking',
                'rate_ranking', 'rate',
                'score', 'stars', 'total_order',
            ]], on=['receiver_province_code', 'receiver_district_code', 'carrier_id', 'new_type'], how='left'
        )
    )
    return result_df


def calculate_service_fee(input_df, cuoc_phi_df=None):
    """
    Note:
        service_fee tính theo cách join với bảng cước phí,
        sau đó filter lại giá trị trong ngưỡng
        bị Lỗi ArrayMemoryError khi chạy local (không đủ memory để chạy)
    """
    if cuoc_phi_df is None:
        cuoc_phi_df = pd.read_parquet(ROOT_PATH + '/processed_data/cuoc_phi.parquet')
        cuoc_phi_df = cuoc_phi_df[['carrier', 'order_type', 'gt', 'lt_or_eq', 'price']]

    input_df.loc[input_df['weight'] > 50000, 'weight'] = 50000
    result_df = input_df.merge(cuoc_phi_df, on=['carrier', 'order_type'], how='inner')
    result_df = result_df.loc[
        (result_df['weight'] > result_df['gt']) &
        (result_df['weight'] <= result_df['lt_or_eq'])
        ]

    # Ninja Van lấy tận nơi cộng cước phí 1,500
    result_df.loc[
        result_df['carrier'].isin(['Ninja Van']) &
        result_df['pickup_type'].isin(['Lấy Tận Nơi']),
        'price'
    ] = result_df['price'] + 1500

    # GHN lấy tận nơi cộng cước phí 1,000
    result_df.loc[
        result_df['carrier'].isin(['GHN']) &
        result_df['pickup_type'].isin(['Lấy Tận Nơi']),
        'price'
    ] = result_df['price'] + 1000

    return result_df.drop(['gt', 'lt_or_eq'], axis=1)


def get_cuoc_phi(cuoc_phi_df, carrier, order_type, weight):
    service_fee = cuoc_phi_df.loc[
        (cuoc_phi_df['carrier'] == carrier)
        & (cuoc_phi_df['order_type'] == order_type)
        & (cuoc_phi_df['gt'] < weight)
        & (cuoc_phi_df['lt_or_eq'] >= weight)
        ]['price'].values[0]
    return service_fee


def calculate_service_fee_v2(input_df):
    cuoc_phi_df = pd.read_parquet(ROOT_PATH + '/processed_data/cuoc_phi.parquet')
    cuoc_phi_df = cuoc_phi_df[['carrier', 'order_type', 'gt', 'lt_or_eq', 'price']]

    input_df.loc[input_df['weight'] > 50000, 'weight'] = 50000
    result_df = input_df.copy()
    result_df['price'] = result_df.apply(
        lambda s: get_cuoc_phi(cuoc_phi_df, s['carrier'], s['order_type'], s['weight']),
        axis=1
    )

    # Ninja Van lấy tận nơi cộng cước phí 1,500
    result_df.loc[
        result_df['carrier'].isin(['Ninja Van']) &
        result_df['pickup_type'].isin(['Lấy Tận Nơi']),
        'price'
    ] = result_df['price'] + 1500

    # GHN lấy tận nơi cộng cước phí 1,000
    result_df.loc[
        result_df['carrier'].isin(['GHN']) &
        result_df['pickup_type'].isin(['Lấy Tận Nơi']),
        'price'
    ] = result_df['price'] + 1000

    return result_df


def calculate_service_fee_v3(input_df):
    target_df = input_df.copy()
    target_df.loc[target_df['weight'] > 50000, 'weight'] = 50000

    cuoc_phi_df = pd.read_parquet(ROOT_PATH + '/processed_data/cuoc_phi.parquet')
    cuoc_phi_df = cuoc_phi_df[['carrier', 'order_type', 'gt', 'lt_or_eq', 'price']]

    cuoc_phi_df1 = cuoc_phi_df.loc[(cuoc_phi_df['lt_or_eq'] <= 1000)]
    cuoc_phi_df2 = cuoc_phi_df.loc[(cuoc_phi_df['gt'] >= 1000) & (cuoc_phi_df['lt_or_eq'] <= 5000)]
    cuoc_phi_df3 = cuoc_phi_df.loc[(cuoc_phi_df['gt'] >= 5000) & (cuoc_phi_df['lt_or_eq'] <= 10000)]
    cuoc_phi_df4 = cuoc_phi_df.loc[(cuoc_phi_df['gt'] >= 10000) & (cuoc_phi_df['lt_or_eq'] <= 50000)]

    target_df1 = target_df.loc[(target_df['weight'] <= 1000)]
    target_df2 = target_df.loc[(target_df['weight'] > 1000) & (target_df['weight'] <= 5000)]
    target_df3 = target_df.loc[(target_df['weight'] > 5000) & (target_df['weight'] <= 10000)]
    target_df4 = target_df.loc[(target_df['weight'] > 10000) & (target_df['weight'] <= 50000)]

    result_df1 = calculate_service_fee(target_df1, cuoc_phi_df1)
    result_df2 = calculate_service_fee(target_df2, cuoc_phi_df2)
    result_df3 = calculate_service_fee(target_df3, cuoc_phi_df3)
    result_df4 = calculate_service_fee(target_df4, cuoc_phi_df4)

    result_df = pd.concat([result_df1, result_df2, result_df3, result_df4], ignore_index=True)

    return result_df


def calculate_notification(input_df):
    re_nhat_df = input_df.groupby(['order_code'])['price'].min().reset_index()
    re_nhat_df['notification'] = 'Rẻ nhất'

    # Gắn ngược lại để lấy đủ row (trong trường hợp có nhiều carrier cùng mức giá
    re_nhat_df = re_nhat_df.merge(input_df, on=['order_code', 'price'], how='inner')

    remain_df1 = merge_left_only(input_df, re_nhat_df, keys=['order_code', 'price'])

    nhanh_nhat_df = remain_df1.groupby(['order_code'])['time_data'].min().reset_index()
    nhanh_nhat_df['notification'] = 'Nhanh nhất'
    nhanh_nhat_df = nhanh_nhat_df.merge(remain_df1, on=['order_code', 'time_data'],
                                        how='inner')

    remain_df2 = merge_left_only(remain_df1, nhanh_nhat_df,
                                 keys=['order_code', 'time_data'])

    hieu_qua_nhat_df = remain_df2.groupby(['order_code'])['score'].max().reset_index()
    hieu_qua_nhat_df['notification'] = 'Dịch vụ tốt'
    hieu_qua_nhat_df = hieu_qua_nhat_df.merge(remain_df2, on=['order_code', 'score'], how='inner')

    remain_df3 = merge_left_only(remain_df2, hieu_qua_nhat_df, keys=['order_code', 'score'])
    remain_df3['notification'] = 'Bình thường'

    result_df = pd.concat([
        re_nhat_df,
        nhanh_nhat_df,
        hieu_qua_nhat_df,
        remain_df3
    ], ignore_index=True)

    return result_df


def calculate_notification_v2(input_df):
    result_df = input_df.copy()
    result_df['price_ranking'] = result_df.groupby('order_code')['price'].rank(method="dense", ascending=True)
    result_df['price_ranking'] = result_df['price_ranking'].astype(int)

    return result_df


def partner_best_carrier_old(data_api_df, threshold=15):
    df1 = data_api_df.loc[data_api_df['total_order'] > threshold]
    df2 = data_api_df.loc[(data_api_df['total_order'] >= 1) & (data_api_df['total_order'] <= threshold)]
    df3 = data_api_df.loc[data_api_df['total_order'] == 0]

    group1 = (
        df1.sort_values(['price', 'rate'], ascending=[True, False])
            .drop_duplicates(['receiver_province', 'receiver_district', 'order_type'], keep='first')
        [['receiver_province', 'receiver_district', 'order_type', 'carrier']]
            .rename(columns={'carrier': 'partner_best_carrier'})
    )
    group2 = (
        df2.sort_values(['rate', 'price'], ascending=[False, True])
            .drop_duplicates(['receiver_province', 'receiver_district', 'order_type'], keep='first')
        [['receiver_province', 'receiver_district', 'order_type', 'carrier']]
            .rename(columns={'carrier': 'partner_best_carrier'})
    )
    group3 = df3[['receiver_province', 'receiver_district', 'order_type']].drop_duplicates()
    group3['partner_best_carrier'] = PARTNER_BEST_CARRIER_DEFAULT

    partner_best_carrier_df = pd.concat([group1, group2, group3]).drop_duplicates(
        ['receiver_province', 'receiver_district', 'order_type'], keep='first')
    partner_best_carrier_df['for_partner'] = partner_best_carrier_df['partner_best_carrier'].map(
        MAPPING_CARRIER_ID)

    return partner_best_carrier_df


def partner_best_carrier(data_api_df):
    data_api_df['wscore'] = data_api_df['price_ranking'] * 1.4 + data_api_df['rate_ranking'] * 1.2 + \
                            data_api_df['score_ranking']
    partner_best_carrier_df = (
        data_api_df.sort_values([
            'receiver_province_code', 'receiver_district_code', 'new_type', 'wscore'
        ]).drop_duplicates(['receiver_province_code', 'receiver_district_code', 'new_type'])
        [['receiver_province_code', 'receiver_district_code', 'new_type', 'carrier']]
            .rename(columns={'carrier': 'partner_best_carrier'})
    )
    data_api_df = data_api_df.merge(partner_best_carrier_df,
                                    on=['receiver_province_code', 'receiver_district_code', 'new_type'], how='inner')
    data_api_df['for_partner'] = data_api_df['partner_best_carrier'].map(MAPPING_CARRIER_ID)

    return data_api_df.drop(['wscore'], axis=1)


def out_data_final(input_df=None, carriers=ACTIVE_CARRIER, show_logs=False):
    if input_df is None:
        giao_dich_valid = pd.read_parquet(ROOT_PATH + '/processed_data/giao_dich_combine_valid.parquet')
        giao_dich_valid = giao_dich_valid[[
            'order_code', 'weight', 'pickup_type', 'sender_province', 'sender_district',
            'receiver_province', 'receiver_district'
        ]]
        focus_df = (
            giao_dich_valid.merge(
                PROVINCE_MAPPING_DISTRICT_DF.rename(columns={
                    'province_code': 'sender_province_code',
                    'district_code': 'sender_district_code',
                    'province': 'sender_province',
                    'district': 'sender_district'
                }), on=['sender_province', 'sender_district'], how='left')
                .merge(
                PROVINCE_MAPPING_DISTRICT_DF.rename(columns={
                    'province_code': 'receiver_province_code',
                    'district_code': 'receiver_district_code',
                    'province': 'receiver_province',
                    'district': 'receiver_district',
                }), on=['receiver_province', 'receiver_district'], how='left')
        )

        focus_df = focus_df[[
            'order_code', 'weight', 'pickup_type', 'sender_province_code', 'sender_district_code',
            'receiver_province_code', 'receiver_district_code'
        ]]
        focus_df['pickup_type'] = focus_df['pickup_type'].fillna('Gửi Bưu Cục')

        assert len(giao_dich_valid) == len(focus_df), 'Transform data sai'
    else:
        focus_df = input_df.copy()
    print('Số dòng input dữ liệu: ', len(focus_df))

    print('i. Tính toán order_type')
    tmp_df1 = generate_order_type(focus_df, carriers=carriers)
    assert len(tmp_df1) == len(focus_df) * len(carriers), 'Transform data sai'

    print('ii. Gắn thông tin tính toán từ API')
    tmp_df2 = combine_info_from_api(tmp_df1, show_logs=show_logs)
    assert len(tmp_df2) == len(tmp_df1), 'Transform data sai'

    print('iii. Tính phí dịch vụ')
    if input_df is None:
        tmp_df3 = calculate_service_fee_v3(tmp_df2)
    else:
        tmp_df3 = calculate_service_fee(tmp_df2)
    assert len(tmp_df3) == len(tmp_df2), 'Transform data sai'

    print('iv. Tính ranking nhà vận chuyển theo tiêu chí rẻ nhất')
    tmp_df4 = calculate_notification_v2(tmp_df3)
    assert len(tmp_df4) == len(tmp_df3), 'Transform data sai'

    print('v. Tính nhà vận chuyển tốt nhất cho đối tác')
    final_df = partner_best_carrier(tmp_df4)
    assert len(final_df) == len(tmp_df4), 'Transform data sai'

    if input_df is None:
        print('vi. Lưu data tính toán...')
        final_df = final_df[API_FULL_COLS]
        if not os.path.exists(ROOT_PATH + '/output'):
            os.makedirs(ROOT_PATH + '/output')
        final_df.to_parquet(ROOT_PATH + '/output/data_check_output.parquet')
    else:
        final_df = final_df[API_COLS]
    print('-' * 100)

    return final_df


if __name__ == '__main__':
    out_data_final()
