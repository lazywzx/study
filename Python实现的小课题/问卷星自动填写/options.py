import xpath as xp


def options_control(k):
    # 调整每个选项的个数
    # 第一题
    if k < 8:
        xpath1 = xp.xpath1_gove
    elif k < 18:
        xpath1 = xp.xpath1_shangye
    elif k < 38:
        xpath1 = xp.xpath1_tea
    elif k < 63:
        xpath1 = xp.xpath1_skill
    elif k < 93:
        xpath1 = xp.xpath1_other
    elif k < 143:
        xpath1 = xp.xpath1_wunong
    else:
        xpath1 = xp.xpath1_stu

    # 第二题
    if k < 43:
        xpath2 = xp.xpath2_1w
    elif k < 163:
        xpath2 = xp.xpath2_1w2w
    elif k < 213:
        xpath2 = xp.xpath2_2w5w
    else:
        xpath2 = xp.xpath2_5w

    # 第三题
    if k < 23:
        xpath3 = xp.xpath3_bad
    elif k < 73:
        xpath3 = xp.xpath3_good
    elif k < 133:
        xpath3 = xp.xpath3_just
    else:
        xpath3 = xp.xpath3_ok

    # 第四题
    if k < 13:
        xpath4 = xp.xpath4_good
    elif k < 58:
        xpath4 = xp.xpath4_bad
    elif k < 140:
        xpath4 = xp.xpath4_just
    else:
        xpath4 = xp.xpath4_ok

    # 第五题
    if k < 28:
        xpath5 = xp.xpath5_good
    elif k < 88:
        xpath5 = xp.xpath5_ok
    elif k < 148:
        xpath5 = xp.xpath5_bad
    else:
        xpath5 = xp.xpath5_just

    # 第六题（多选只能按单选处理）
    if k < 12:
        xpath6 = xp.xpath6_qita
    elif k < 27:
        xpath6 = xp.xpath6_tanfu
    elif k < 47:
        xpath6 = xp.xpath6_xiaoyuan
    elif k < 80:
        xpath6 = xp.xpath6_guannian
    elif k < 130:
        xpath6 = xp.xpath6_yingjian
    elif k < 180:
        xpath6 = xp.xpath6_jiaoyu
    else:
        xpath6 = xp.xpath6_shizi

    # 第七题
    if k < 23:
        xpath7 = xp.xpath7_xuanhao
    elif k < 33:
        xpath7 = xp.xpath7_gongan
    elif k < 58:
        xpath7 = xp.xpath7_zhuanbian
    elif k < 98:
        xpath7 = xp.xpath7_jinyi
    elif k < 143:
        xpath7 = xp.xpath7_shehui
    elif k < 180:
        xpath7 = xp.xpath7_heli
    else:
        xpath7 = xp.xpath7_guojia

    # 第八题
    if k < 8:
        xpath8 = xp.xpath8_poyu
    elif k < 20:
        xpath8 = xp.xpath8_wancheng
    elif k < 35:
        xpath8 = xp.xpath8_buzhidao
    elif k < 45:
        xpath8 = xp.xpath8_dajia
    elif k < 127:
        xpath8 = xp.xpath8_weile
    else:
        xpath8 = xp.xpath8_gaibian

    # 第九题
    if k < 1:
        xpath9 = xp.xpath9_jiating
    elif k < 4:
        xpath9 = xp.xpath9_teshu
    elif k < 16:
        xpath9 = xp.xpath9_renwei
    elif k < 48:
        xpath9 = xp.xpath9_xuexi
    else:
        xpath9 = xp.xpath9_meiyou

    # 第十题
    if k < 7:
        xpath10 = xp.xpath10_gaoxiao
    elif k < 15:
        xpath10 = xp.xpath10_qita
    elif k < 23:
        xpath10 = xp.xpath10_shengyuan
    elif k < 35:
        xpath10 = xp.xpath10_yingyang
    elif k < 50:
        xpath10 = xp.xpath10_bushi
    elif k < 70:
        xpath10 = xp.xpath10_liangmian
    elif k < 83:
        xpath10 = xp.xpath10_zhuxue
    elif k < 120:
        xpath10 = xp.xpath10_zaiyou
    elif k < 180:
        xpath10 = xp.xpath10_gaozhong
    else:
        xpath10 = xp.xpath10_mianchu

    # 第十一题
    if k < 32:
        xpath11 = xp.xpath11_yiban
    elif k < 180:
        xpath11 = xp.xpath11_tuchu
    else:
        xpath11 = xp.xpath11_jihu

    # 第十二题
    if k < 140:
        xpath12 = xp.xpath12_henshao
    elif k < 180:
        xpath12 = xp.xpath12_meiyou
    elif k < 205:
        xpath12 = xp.xpath12_xueyi
    elif k < 220:
        xpath12 = xp.xpath12_qiyi
    else:
        xpath12 = xp.xpath12_qiliang

    # 第十三题
    if k < 188:
        xpath13 = xp.xpath13_you
    elif k < 198:
        xpath13 = xp.xpath13_mei
    else:
        xpath13 = xp.xpath13_yi

    return xpath1, xpath2, xpath3, xpath4, xpath5, xpath6, xpath7, xpath8, xpath9, xpath10, xpath11, xpath12, xpath13
