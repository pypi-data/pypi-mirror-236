import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
from tqdm import *

class single_signal_test(object):
    def __init__(self) -> None:
        pass
    
    def cal_turnover(self,df,ndays):
        # holdings:
        # pd.Series
        # multiindex: timestamp,code
        # 值都是1
        holdings = df.copy()
        holdings = holdings.unstack().dropna(how ='all',axis = 1)
        holdings = holdings.apply(lambda x: x/x.sum(),axis = 1)
        holdings = holdings.fillna(0)
        return (holdings.diff(ndays).abs().sum(axis = 1)/2)
    
    def cal_holdingnums(self,df):
        # holdings:
        # pd.Series
        # multiindex: timestamp,code
        # 值都是1
        holdings = df.copy()
        holdings = holdings.groupby(level = 0).sum()
        return holdings

    def one_factor_grouper(self,df,factorname,quantiles,qcut): # 分组
        # concatdf:pd.DataFrame
        # factorname: str
        # multiindex: timestamp,code
        # columns: nday_return, factorname1, factorname2...
        concatdf = df[[factorname]].copy().round(6)# 设置保留小数！
        concatdf[factorname+'_rank'] = concatdf[factorname].groupby(level = 'date', group_keys = False).rank()
        if qcut:
            concatdf[factorname+'_quantile'] =concatdf[factorname+'_rank'].dropna().groupby(level = 'date', group_keys = False).apply(lambda x: pd.qcut(x,quantiles,labels=list(range(1,quantiles+1)))).astype(int)
        else:
            concatdf[factorname+'_quantile'] =concatdf[factorname+'_rank'].dropna().groupby(level = 'date', group_keys = False).apply(lambda x: pd.cut(x,quantiles,labels=list(range(1,quantiles+1)))).astype(int)
        return concatdf

    def one_factor_return(self,df,factorname,ndays,return_col,w_method,demean = False): # 计算分组收益
        if w_method =='average':
            qreturn = df.groupby(level = 'date', group_keys = True).apply(lambda x: x.groupby(factorname+'_quantile')[[return_col]].mean()/ndays).unstack()
            qreturn.columns = [i[1] for i in list(qreturn)]
            
        if w_method == 'factor_weighted':
            tmpdf = df.copy()
            tmpdf['rwf'] = tmpdf[return_col]*tmpdf[factorname]
            tmpdf.dropna(subset = ['rwf'],inplace = True)
            qreturn = tmpdf.groupby(level = 'date', group_keys = True).\
                apply(lambda x: x.groupby(factorname+'_quantile').\
                      apply(lambda x: x['rwf'].sum()/x[factorname].sum() if x[factorname].sum()>0 else 0)/ndays)       
            # qreturn = tmpdf.groupby(level = 'date', group_keys = True).\
            #     apply(lambda x: x.groupby(factorname+'_quantile').\
            #           apply(lambda x: (x[return_col]*x[factorname]).sum()/x[factorname].sum())/ndays)      
            
        if w_method =='cap_weighted':
            qreturn = df.groupby(level = 'date', group_keys = True).\
                apply(lambda x: x.groupby(factorname+'_quantile').\
                      apply(lambda x: (x[return_col]*x['cap']).sum()/x['cap'].sum())/ndays)

        if len(qreturn.index.names)==1:
            pass
        else:
            qreturn= qreturn.unstack().apply(lambda x: x.fillna(x.mean()),axis = 1)     

        if demean:
            qreturn = qreturn.apply(lambda x: x-x.mean(),axis = 1)
        return qreturn
    
    def one_factor_icir(self,df,factorname,return_col):
        from scipy import stats
        ic = df.groupby(level = 'date').apply(lambda x: x[[return_col,factorname]].corr('spearman'))
        ic_org = ic[ic.index.get_level_values(1) ==return_col][factorname].dropna()
        ictable = ic_org.describe()[['count','mean','std','min','max']].copy()
        ictable['risk_adj'] = ic_org.mean()/ic_org.std()
        ictable['skew'] = ic_org.skew()
        ictable['kurtosis'] = ic_org.kurtosis()
        if ictable['mean'] <0:
            ictable['p-value'] = stats.ttest_1samp(ic_org,0,alternative='less').pvalue
        else:
            ictable['p-value'] = stats.ttest_1samp(ic_org,0,alternative='greater').pvalue
        return ictable

    def one_factor_ret_sharp(self,qreturn,ret_freq):
        return qreturn.mean()/qreturn.std()*np.sqrt(252/ret_freq)
    
    def factor_prepare(self,allfactors,fc,quantiles,qcut):
        test_fc = allfactors[[fc]].copy().rename_axis(['date','symbol'])
        res_df = self.one_factor_grouper(test_fc,fc,quantiles,qcut)# 序数标准化
        return res_df
    
    def factor_ret_test_sheet(self,
                              weight_method,
                              index_price, #'''基准日期是timestamp'''
                              fcname,
                              res_df,
                              Price,
                              days,
                              savedir,
                              demean = False):
        from alphalens import utils
        plottools = plot_tools()
        mate_al = mate_alphalens()
        tov_df = res_df.groupby(by = fcname+'_quantile').apply(lambda x: self.cal_turnover(x[fcname+'_quantile']/x[fcname+'_quantile'],days))
        if len(tov_df.index.names)==1:
            to = tov_df.mean(axis =1)
        else:
            to = tov_df.unstack().mean(axis = 1)
        clean_factor,price = mate_al.index_mate(res_df.dropna(),Price)
        fwr = utils.compute_forward_returns(price.stack(),price)
        clean_factor[str(days)+'D'] = fwr[str(days)+'D']
        clean_factor = clean_factor.reset_index()
        clean_factor['date'] = clean_factor['date'].astype(str)
        clean_factor = clean_factor.set_index(['date','asset']).dropna()
        if index_price is not None:
            clean_factor = mate_al.trans_ex_return(clean_factor,index_price,ret_col=[str(days)+'D'])
        else:
            clean_factor[str(days)+'D'] = clean_factor.groupby(level = 'date',group_keys = False).apply(lambda x: x[str(days)+'D']-x[str(days)+'D'].mean())
        qreturn = self.one_factor_return(clean_factor,fcname,days,str(days)+'D',w_method = weight_method,demean=demean)

        # ic
        ic_table = self.one_factor_icir(clean_factor,fcname,str(days)+'D')
        indicators = self.judge_material(qreturn,ic_table,days)
        plottools.factor_plt(qreturn,to,indicators,fcname,days,savedir)
        return qreturn,clean_factor,indicators
    
    def judge_material(self,qreturn,ic_table,days):
        from scipy import stats
        indicators = ic_table.copy()
        maxquantile = max(qreturn.columns)
        lsret = qreturn[maxquantile] - qreturn[1]
        groupmean = qreturn.mean(axis = 0)
        groupmean_diff = groupmean.diff().dropna()
        top_half = groupmean_diff.iloc[-5:]

        top_sharp = qreturn[maxquantile].mean()/qreturn[maxquantile].std()*pow(252/days,1/2)
        t,p_lsret =stats.ttest_1samp(lsret,0,alternative='greater')
        t,p_groupmean =stats.ttest_1samp(groupmean_diff,0,alternative='greater')
        t,p_tophalfmean = stats.ttest_1samp(top_half,0,alternative='greater')

        indicators['TopQtl_SR'] = top_sharp
        indicators['LSRet_pvalue'] = p_lsret
        indicators['MeanRetDiff_pvalue'] = p_groupmean
        indicators['TophalfMeanRetDiff_pvalue'] = p_tophalfmean
        return indicators

    def efficient_judge(self,indicators):
        from scipy import stats
         # 因子判别
        '''
        检验:
        对两个都通过的是有用的因子
        '''
        if indicators['p-value']<= 0.05 and indicators['TopQtl_SR']>=1:
            if indicators['TophalfMeanRetDiff_pvalue']<=0.3 and indicators['LSRet_pvalue']<=0.12:
                # print(fc+'有用;头部{}组平均收益一阶差分p值{},多空收益p值{},ic_pvalue{},top组超额夏普{}'.format(int(maxquantile/2),p_top_halfmean,p_lsret))
                return 1
            # 且两个乘起来能跟原来的匹配；且另一个不能太差
            # elif indicators['TophalfMeanRetDiff_pvalue']*indicators['LSRet_pvalue']<0.0025 and (indicators['TophalfMeanRetDiff_pvalue']/0.05 <= 0.1 or indicators['LSRet_pvalue']/0.05 <= 0.1) \
            #     and min(indicators['MeanRetDiff_pvalue'],indicators['TophalfMeanRetDiff_pvalue'])<=0.05 and indicators['TophalfMeanRetDiff_pvalue']<0.3:
                # print(fc+'勉强有用;头部{}组平均收益一阶差分p值{},整体平均收益一阶差分p值{},多空收益p值{}'.format(int(maxquantile/2),p_top_halfmean,p_groupmean,p_lsret))
            else:
                return 2           
        return 0

    def eff_classification(self,fc,indicator,judgefunc,strict_eff,unstrict_eff):
        '''
        输入:
        因子矩阵
        
        输出:
        1、因子测试结果
        2、噪声因子
        '''
        # 因子判别
        if judgefunc(indicator) == 1:
            strict_eff.append(fc)
            unstrict_eff.append(fc)
        elif judgefunc(indicator) == 2:
            unstrict_eff.append(fc)

        return strict_eff,unstrict_eff

class multi_factor_test(object):
    def __init__(self) -> None:
        self.sst = single_signal_test()
        pass

    def factors_abnormal_ret(self,factordf,return_col,factorlist,days,index_price = None,pricedf = None,longshort_return = False):
        df = factordf.copy()
        if pricedf is not None:
            # 默认明收除今收
            df[str(days)+'D'] = pricedf.pct_change(days,fill_method = None).shift(-days).stack()
            if index_price is not None:
                ml = mate_alphalens()
                df,pricedf = ml.index_mate(df,pricedf)
                df = ml.trans_ex_return(df,index_price,str(days)+'D')
            df = df.rename(columns = {str(days)+'D':return_col+str(days)+'D'}).dropna(subset = return_col+str(days)+'D')
        if longshort_return == False:
            ret_k = df.groupby(level = 'date',group_keys = False).apply(lambda x: sm.formula.ols(return_col+str(days)+'D'+'~'+'+'.join(factorlist),data = x).fit().params)
            del ret_k['Intercept']
        else :
            lscol = list(factordf)
            quantiles = int(df[return_col+str(days)+'D'].groupby(level = 'date').count().mean()//100)
            LSretList = []
            for col in tqdm(lscol):
                tmpdf = df.copy()
                tmpdf[col+'_quantile'] = self.sst.one_factor_grouper(df,col,quantiles,False)[col+'_quantile']
                qreturn = self.sst.one_factor_return(tmpdf,col,days,'ret{}D'.format(days),'factor_weighted',False)
                LSretList.append(qreturn[max(list(qreturn))] - qreturn[1])
            ret_k = pd.concat(LSretList,axis = 1)
            ret_k.columns = lscol
        return ret_k

    def multif_barra_norm(self,allfactors,Bft):
        df = allfactors.copy()
        print('barra中性化....')
        for fcname in tqdm(list(df)):
            test_fc = df[[fcname]].copy().rename_axis(['date','symbol'])
            residual_ols,params_ols = Bft.barra_compose(test_fc)
            df[fcname] = residual_ols # 中性化之后的因子替换原始因子
        return df

    def multif_industry_norm(self,allfactors,industry_info):
        df = allfactors.copy()
        df['first_industry_name'] = industry_info
        df = df.dropna(subset = 'first_industry_name').groupby(level = 'date',group_keys =False).apply(lambda x: x.groupby(by = 'first_industry_name',group_keys =False).apply(lambda x:x-x.mean(numeric_only=True)))
        del df['first_industry_name']
        return df


    def multif_corr_ana(self,df,factornamelist): # 多因子相关性分析
        # df:pd.DataFrame
        # factornamelist: strlist
        # multiindex: timestamp,code
        # columns: nday_return, factorname1, factorname2...
        df_ana = df[factornamelist].groupby(level = 'date').corr()
        corr_mean = df_ana.groupby(level = 1).mean() # corr之后的矩阵第二层没名字，所以用1来表示；第二层是因子名
        corr_ir = df_ana.groupby(level = 1).mean()/df_ana.groupby(level = 1).std()  
        return corr_mean.loc[list(corr_mean)],corr_ir.loc[list(corr_ir)]

    def multif_pca_ana(self,originalFactor,domain_factor_nums): # 多因子pca分析
        # originalFactor: pd.DataFrame
        # multiindex: timestamp,code
        # columns: factorname1, factorname2...
        from sklearn import preprocessing
        data = originalFactor.groupby(level = 'date', group_keys = False).apply(lambda x: preprocessing.scale(x))
        data = np.vstack(data.values)
        from sklearn.decomposition import PCA
        pcaModel = PCA(domain_factor_nums)
        pcaModel.fit(data)
        pcaFactors = pcaModel.transform(data)
        pcaFactors = pd.DataFrame(pcaFactors)
        pcaFactors.index = originalFactor.index
        pcaFactors.columns = ['pca_'+str(i) for i in range(domain_factor_nums)]
        return pcaModel.explained_variance_,pcaModel.explained_variance_ratio_,pcaFactors

    def batch_factors_test(self,weight_method,allfactors,Price,quantiles,days,qcut,savedir,index_price = None,demean = False):
        returndict = {}
        sst = single_signal_test()
        for fc in tqdm(list(allfactors)):
            res_df = sst.factor_prepare(allfactors,fc,quantiles,qcut)
            sst.factor_ret_test_sheet(weight_method,index_price,fc,res_df,Price,days,savedir,demean)
            returndict[fc] = res_df[[fc]]
        return returndict

    def multif_tsstable_test(self,originalData):
        # originalFactor: pd.DataFrame
        # multiindex: timestamp,code
        # columns: factorname1, factorname2...
        from statsmodels.tsa.stattools import adfuller
        data = originalData.copy()#.groupby(level = 0).apply(lambda x: (x-x.mean())/x.std())不要再标准化了！！
        mean_pvalue = data.groupby(level = 'date').apply(lambda x:x.mean()).apply(lambda x: adfuller(x)[1])
        std_pvalue = data.groupby(level = 'date').apply(lambda x:x.std()).apply(lambda x: adfuller(x)[1])
        skew_pvalue = data.groupby(level = 'date').apply(lambda x:x.skew()).apply(lambda x: adfuller(x)[1])
        kurt_pvalue = data.groupby(level = 'date').apply(lambda x:x.kurt()).apply(lambda x: adfuller(x)[1])
        yarn_pvalue = pd.concat([mean_pvalue,std_pvalue,skew_pvalue,kurt_pvalue],axis = 1)
        yarn_pvalue.columns = ['mean','std','skew','kurt']
        return yarn_pvalue
    
    def del_updown_limit(self,factordf,daybar,text):
        # 剔除涨跌停
        notuplimit = daybar[~(daybar[text] == daybar.limit_up)]
        notdownlimit = daybar[~(daybar[text] == daybar.limit_down)]
        factordf = factordf[factordf.index.isin(notuplimit.index)]
        factordf = factordf[factordf.index.isin(notdownlimit.index)]
        return factordf

    def in_some_pool(self,df,pool_components):
        factordf = df.copy()
        factordf['inpool']=pool_components.applymap(lambda x:1)
        factordf['inpool'] = factordf['inpool'].apply(lambda x: 1 if x>0 else 0)
        testdf = factordf[factordf['inpool']>=1]
        del testdf['inpool']
        return testdf
    
    def orthog(self,factor_mat, y, xlist):
        df = factor_mat.replace([np.inf, -np.inf], np.nan).dropna()
        regre = sm.formula.ols(y+'~'+'+'.join(xlist),data = df).fit()
        params = regre.params[~(regre.params.index == 'Intercept')]
        intercept = regre.params[(regre.params.index == 'Intercept')]
        residual = df[y] - (df[list(params.index)]*params).sum(axis = 1) - intercept.values
        residual = pd.DataFrame(residual)
        residual.columns = [y]
        return self.mat_normlize(residual),params
    
    def mat_orthog(self,factor_mat):
        print(factor_mat.index[0][0])
        temp1 = factor_mat.replace([np.inf, -np.inf], np.nan).dropna()
        for i in list(temp1):
            no = list(temp1).index(i)
            if no==0:
                temp1[i] = self.mat_normlize(temp1[i])
                continue
            fclist = list(filter(lambda x: x!=i,list(temp1)[:no]))
            temp1[i] = self.orthog(temp1,i,fclist)[0]
        return temp1
    
    def ts_mat_orthog(self,factor_mat):
        return factor_mat.groupby(level = 'date',group_keys = False).apply(self.mat_orthog)
    
    def mat_normlize(self,factor_mat):
        df = factor_mat.rename_axis(['date','symbol']).replace([np.inf, -np.inf], np.nan)
        def norm(x):
            return (x - x.min())/(x.max()-x.min())
        return df.groupby(level = 'date',group_keys = False).apply(norm)

    def mat_ranknormlize(self,factor_mat):
        df = factor_mat.rename_axis(['date','symbol']).replace([np.inf, -np.inf], np.nan)
        def norm(x):
            x_rank = x.rank()
            return (x_rank - x_rank.min())/(x_rank.max()-x_rank.min())
        return df.groupby(level = 'date',group_keys = False).apply(norm)

    def multindex_shift(self,fcdf):
        df = fcdf.reset_index()
        datelist = list(df['date'].drop_duplicates())
        datedict = dict(zip(datelist[:-1],datelist[1:]))
        df['date'] =df['date'].apply(lambda x: datedict[x] if x in datedict.keys() else np.nan)
        return df.dropna(subset = 'date').set_index(['date','symbol'])

class Barra_factor_ana(object):
    '''
    1. growth要求至少504天的数据，部分股票不满足该条件会导致在因子整合到一起的时候被剔除
    2. barrafactor必须为双重索引，且第一重索引是日期，第二重索引是标的
    '''
    def __init__(self,df=None,start_date=None,end_date=None,dir=None,skip_fileload=None) -> None:
        # 预加载数据
        if not skip_fileload:
            self.price = df
            dailyreturn = df/df.shift(1)-1
            dailyreturn.dropna(how = 'all',inplace=True)
            self.returndata = dailyreturn
            self.start_date = start_date
            self.end_date = end_date
            import os
            filelist = os.listdir(dir)
            self.filedict = {}
            for f in filelist:
                if f[-3:]=='csv':
                    self.filedict[f[:-4]] = pd.read_csv(dir+f,index_col = [0,1])
            pass

    def rise_barra_factors(self):
        print('rise size')
        self.size = np.log(self.filedict['market_cap']).dropna()
        def OLSparams(y,x):
            print('rise beta')
            X_ = x.droplevel('order_book_id')
            df = y.copy()
            df['market_r'] = X_['r']
            df.dropna(subset = 'market_r',inplace = True)
            dflist = list(df.rolling(252))[252:]
            paramslist = []
            for olsdf in dflist:
                mod = sm.OLS(olsdf,sm.add_constant(olsdf['market_r']))
                re = mod.fit()
                params = re.params.T
                params.index = olsdf.columns
                params = params[params.index!='market_r']
                params['date'] = olsdf.index[-1]
                params = params.rename(columns = {'market_r':'beta'})
                paramslist.append(params)
            olsparams = pd.concat(paramslist).set_index('date',append=True).unstack().T
            constdf = olsparams.loc['const'].ewm(halflife = 63,ignore_na = True,adjust = False).mean().stack()
            betadf = olsparams.loc['beta'].ewm(halflife = 63,ignore_na = True,adjust = False).mean().stack()
            # cal residual
            mkt_df = pd.concat([X_['r']]*len(list(betadf.unstack())),axis = 1)
            mkt_df.columns = list(betadf.unstack())
            residual = y - betadf.unstack()*mkt_df - constdf.unstack() # 这里的residual已经是经过ewm的beta和const计算得到的就不用再ewm了
            return {'beta':betadf,'const':constdf,'residual':residual}
        def MOMTM(y):
            df = np.log(1+y)
            momtm = df.ewm(halflife=126,ignore_na = True,adjust = False).mean()#.iloc[-1:]
            return momtm
        def CMRA(y,T):
            date = y.index[-1]
            dflist= []
            for i in range(1,T+1):
                pct_n_month = pd.DataFrame((y/y.shift(21*i)-1).iloc[-1])/21
                dflist.append(pct_n_month)
            df = pd.concat(dflist,axis =1)
            zmax = df.max(axis =1)
            zmin = df.min(axis = 1)
            cmra = pd.DataFrame(np.log(1+zmax)-np.log(1+zmin),columns = [date]).T
            return cmra
        def orthog(barrafactor,y,xlist):
            df = barrafactor.copy()
            regre = sm.formula.ols(y+'~'+'+'.join(xlist),data = df).fit()
            for p in xlist:
                df[p]*= regre.params[p]
            df[y+'_orth'] = df[y] - df[xlist].sum(axis = 1)-regre.params['Intercept']
            return df[[y+'_orth']]

        # beta
        self.olsparams = OLSparams(self.returndata,self.filedict['market_r'])
        self.beta = pd.DataFrame(self.olsparams['beta']).dropna()
        self.beta.columns = ['beta']
        
        # momentum
        print('rise momentum')
        # retroll504 = list(self.returndata.rolling(504))[504:]
        # self.momtm = pd.concat(list(map(lambda x: MOMTM(x),retroll504))).shift(21).dropna(how = 'all')
        self.momtm = MOMTM(self.returndata).shift(21).dropna(how = 'all')
        self.momtm = pd.DataFrame(self.momtm.stack(),columns=['momentum'])

        # residual volatility
        print('rise residual volatility')
        self.hist_volatility = self.returndata.ewm(halflife = 42,ignore_na = True,adjust = False).std().dropna(how = 'all')
        CMRAlist = list(self.price.rolling(252))[252:]
        self.CMRA = pd.concat(list(map(lambda x: CMRA(x,12),CMRAlist)))
        self.Hsigma = self.olsparams['residual'].rolling(252,min_periods = 1).std()
        self.residual_volatility = pd.DataFrame((self.hist_volatility*0.74+self.CMRA*0.16+self.Hsigma*0.1).stack()).dropna()
        self.residual_volatility.columns = ['residual_volatility']

        # non-linear size
        print('rise non-linear size')
        self.nlsize = (self.size**3).dropna()
        self.nlsize.columns = ['nlsize']

        # Bp
        print('rise Bp')
        self.Bp = self.filedict['Bp'].dropna()
        
        # liquidity
        print('rise Liquidity')
        self.tvrdf = self.filedict['turnover']
        self.liq_1m = self.tvrdf.groupby(level = 1, group_keys = False).apply(lambda x: x.sort_index().rolling(22,min_periods =1).mean())
        self.liq_3m = self.tvrdf.groupby(level = 1, group_keys = False).apply(lambda x: x.sort_index().rolling(74,min_periods =1).mean())
        self.liq_12m = self.tvrdf.groupby(level = 1, group_keys = False).apply(lambda x: x.sort_index().rolling(252,min_periods =1).mean())
        self.liq = (0.35*self.liq_1m + 0.35*self.liq_3m + 0.3*self.liq_12m).dropna()

        print('rise Earning Yield')
        self.earning_yield = pd.concat([self.filedict['Ep'],self.filedict['Sp']],axis = 1)
        self.earning_yield['earning_yield'] = self.earning_yield['ep_ratio_ttm']*0.66+self.earning_yield['sp_ratio_ttm']*0.34
        self.earning_yield = self.earning_yield[['earning_yield']].dropna()
        
        # growth
        print('rise growth')
        NP = self.filedict['NPGO'].unstack()
        NP = (NP-NP.shift(504))/NP.shift(504).abs().replace(0,np.nan)
        NP = NP.stack()
        RVN = self.filedict['RGO'].unstack()
        RVN = (RVN - RVN.shift(504))/RVN.shift(504).abs().replace(0,np.nan)
        RVN = RVN.stack()
        self.growth = pd.DataFrame(NP['net_profit_parent_company_ttm_0']*0.34+RVN['revenue_ttm_0']*0.66)
        self.growth.columns = ['growth']
        self.growth.dropna(inplace=True)

        # leverage
        print('rise leverage')
        self.leverage = self.filedict['MLEV']['du_equity_multiplier_ttm']*0.38+self.filedict['DTOA']['debt_to_asset_ratio_ttm']*0.35+self.filedict['BLEV']['book_leverage_ttm']*0.27
        self.leverage = pd.DataFrame(self.leverage)
        self.leverage.columns = ['leverage']
        self.leverage.dropna(inplace=True)

        # concat
        self.barrafactor = pd.concat([
                                    self.size,
                                    self.beta,
                                    self.momtm,
                                    self.residual_volatility,
                                    self.nlsize,
                                    self.Bp,
                                    self.liq,
                                    self.earning_yield,
                                    self.growth,
                                    self.leverage],axis = 1).sort_index(level = 0)
        '''正则化'''
        # 未经正则化的原始因子已存为类变量，可直接调用
        print('Orthogonalizing....')
        y = ['residual_volatility','nlsize','turnover']
        xlist = ['circulation_A','beta']   
        # 不dropna会报错
        self.barrafactor[y[0]] = self.barrafactor[[y[0]]+xlist].dropna().groupby(level = 0, group_keys = False).apply(lambda x: orthog(x,y[0],xlist))
        self.barrafactor[y[1]] = self.barrafactor[[y[1]]+xlist[:1]].dropna().groupby(level = 0, group_keys = False).apply(lambda x: orthog(x,y[1],xlist[:1]))
        self.barrafactor[y[2]] = self.barrafactor[[y[2]]+xlist[:1]].dropna().groupby(level = 0, group_keys = False).apply(lambda x: orthog(x,y[2],xlist[:1]))
        # 标准化
    
    def return_barra_factor(self,rank_normalize:bool):
        mft = multi_factor_test()
        if rank_normalize:
            return mft.mat_ranknormlize(self.barrafactor)
        else:
            return mft.mat_normlize(self.barrafactor)

    def barra_compose(self,factordata):
        # 因子是rank数据
        decompose = pd.concat([self.barrafactor,factordata],axis = 1).dropna().rename_axis(['date','symbol'])
        def orthog(barrafactor,y,xlist):
            df = barrafactor.copy()
            regre = sm.formula.ols(y+'~'+'+'.join(xlist),data = df).fit()
            params = regre.params[~(regre.params.index == 'Intercept')]
            intercept = regre.params[(regre.params.index == 'Intercept')]
            residual = df[y] - (df[list(params.index)]*params).sum(axis = 1) - intercept.values
            return residual,params
        # 这种方法只算一天的会错
        # residual_ols =decompose.groupby(level = 0).apply(lambda x: orthog(x,list(decompose)[-1],list(decompose)[:-1])[0]).droplevel(0)
        # params_ols =decompose.groupby(level = 0).apply(lambda x: orthog(x,list(decompose)[-1],list(decompose)[:-1])[1])
        # return residual_ols,params_ols
        decomposebyday = list(decompose.groupby(level = 'date'))
        residual_olslist = []
        params_olslist = []
        for df in decomposebyday:
            x = df[1]
            residual_ols,params_ols = orthog(x,list(decompose)[-1],list(decompose)[:-1])
            residual_olslist.append(residual_ols)
            params_olslist.append(pd.DataFrame(params_ols,columns = [df[0]]).T)
        return pd.concat(residual_olslist),pd.concat(params_olslist)

    def barra_style_pool(self,style,cutnum):
        bystyle = self.barrafactor[[style]].copy()
        bystyle[style+'_group'] = bystyle[style].dropna().groupby(level = 0,group_keys=False).apply(lambda x: pd.cut(x,cutnum,labels=list(range(1,cutnum+1))))
        return bystyle

    def factor_performance_bystyle(self,factordata,factorname,style,cutnum):
        # 即便因子在风格上没有偏斜，仍然会有不同风格上因子表现不同的情况
        bystyle = pd.concat([factordata,self.barrafactor[[style]]],axis = 1)
        bystyle[style+'_group'] = bystyle[style].dropna().groupby(level = 0,group_keys=False).apply(lambda x: pd.cut(x,cutnum,labels=list(range(1,cutnum+1))))
        ic_daily = bystyle.groupby(style+'_group',group_keys=False).apply(lambda x: x[[factorname,'nday_return']].groupby(level = 0).apply(lambda x: x.corr('spearman').iloc[0,1])).T
        return ic_daily


class AutoMatic(object):
    sst = single_signal_test()
    mft = multi_factor_test()
    def __init__(self,Bft,base_index,Price,quantiles,days,qcut,demean,weighted_method) -> None:
        '''base_index基准价格时间索引是timestamp'''
        self.Bft = Bft
        self.Price = Price.copy()
        self.base_index = base_index
        self.quantiles = quantiles
        self.days = days
        self.qcut = qcut
        self.demean = demean
        self.weighted_method = weighted_method
        pass

    def AutoMatic_DirCheck(self,path):
        if not os.path.exists(path):
            os.makedirs(path)

    def AutoMatic_Direc_Adjust(self,factors,dir_):
        neu_factors = factors.copy()
        direction_dict = {}
        strict_eff = []
        unstrict_eff = []
        self.AutoMatic_DirCheck(dir_+'direction/')
        self.AutoMatic_DirCheck(dir_+'direction/redirection/')
        for fc in list(neu_factors):
            res_df = self.sst.factor_prepare(neu_factors,fc,self.quantiles,self.qcut)
            if self.weighted_method == 'cap_weighted':
                res_df['cap'] = self.cap
                
            qreturn,tmp,indicator = self.sst.factor_ret_test_sheet(self.weighted_method,self.base_index,fc,res_df,self.Price,self.days,dir_+'/direction/',self.demean)
            if qreturn[list(qreturn)[0]].sum()<= qreturn[self.quantiles].sum():
                print(fc+'是正向因子')
                direction_dict[fc] = 1
            if qreturn[list(qreturn)[0]].sum() > qreturn[self.quantiles].sum():
                print(fc+'是负向因子')
                neu_factors = neu_factors.copy()
                neu_factors[fc]=self.mft.mat_normlize(-1*neu_factors[fc])
                direction_dict[fc] = -1

                res_df = self.sst.factor_prepare(neu_factors,fc,self.quantiles,self.qcut)
                if self.weighted_method == 'cap_weighted':
                    res_df['cap'] = self.cap

                qreturn,tmp,indicator = self.sst.factor_ret_test_sheet(self.weighted_method,self.base_index,fc,res_df,self.Price,self.days,dir_+'direction/redirection/',self.demean)
            # 有效性判别
            strict_eff,unstrict_eff = self.sst.eff_classification(fc,indicator,self.sst.efficient_judge,strict_eff,unstrict_eff)
        return direction_dict,strict_eff,unstrict_eff
    
    def AutoMatic_Factor_Merge_Ret(self,neu_factors,base_factors,mergename,dir_):
        base_f = pd.DataFrame(neu_factors[base_factors].sum(axis = 1),columns = [mergename])
        res_df = self.sst.factor_prepare(base_f,mergename,self.quantiles,self.qcut)
        self.AutoMatic_DirCheck(dir_)
        if self.weighted_method == 'cap_weighted':
            res_df['cap'] = self.cap
        qreturn,clean_factor,indicator = self.sst.factor_ret_test_sheet(self.weighted_method,self.base_index,mergename,res_df,self.Price,self.days,dir_,self.demean)  
        return qreturn,clean_factor


    def AutoMatic_Compare_Indicator(self,qreturn,reverse):
        if reverse:
            maxq = min(list(qreturn))
            base_perf_sr = -1*qreturn[maxq].mean()/qreturn[maxq].std()
            return base_perf_sr
        maxq = max(list(qreturn))
        base_perf_sr = qreturn[maxq].mean()/qreturn[maxq].std()
        return base_perf_sr
    
    def threads_pool_run(self,params_batch):
        InSampleFactors,i,dir_ = params_batch[0] , params_batch[1] , params_batch[2]
        import matplotlib
        matplotlib.use('agg')
        savedir = dir_+'{}/'.format(i)
        direction_dict,strict_eff,unstrict_eff =self.AutoMatic_Direc_Adjust(InSampleFactors,savedir) # 方向调整
        return (direction_dict,strict_eff,unstrict_eff)

    def AutoMatic_Stochastic_Optimizer(self,test_factor,threads_num,dir_):
        dateset = list(set(test_factor.index.get_level_values('date')))
        import multiprocessing
        from multiprocessing import Pool
        InSplList = []
        for i in range(threads_num):
            randomdate = sorted(np.random.choice(dateset,int(len(dateset)/5),replace = False))
            InSplList.append((test_factor.loc[randomdate],i,dir_))
        pool = Pool(min(multiprocessing.cpu_count(),threads_num))
        return pool.map(self.threads_pool_run,InSplList)

    def AutoMatic_Perf_InPool(self,neu_factors,base_factors,reverse,save_dir):

        qreturn,tmp =self.AutoMatic_Factor_Merge_Ret(neu_factors,base_factors,'basef',save_dir+'temp/')
        base_perf_sr= self.AutoMatic_Compare_Indicator(qreturn,reverse)
        others = list(filter(lambda x: x not in base_factors,list(neu_factors)))
        for sf in others:# 挨个加表现
            print(base_factors)
            qreturn,tmp =self.AutoMatic_Factor_Merge_Ret(neu_factors,base_factors+[sf],sf+'_basef',save_dir+'temp/')
            perf_sr = self.AutoMatic_Compare_Indicator(qreturn,reverse)
            print('是否超越此前表现:{};本次超额夏普:{},此前最佳超额夏普:{}'.format(perf_sr > base_perf_sr,perf_sr,base_perf_sr))
            if perf_sr > base_perf_sr:
                base_factors.append(sf)
                if perf_sr > base_perf_sr:
                    base_perf_sr = perf_sr
        qreturn,clean_factor = self.AutoMatic_Factor_Merge_Ret(neu_factors,base_factors,'basef',save_dir+'final/')

        return qreturn,clean_factor


class plot_tools(object):
    def __init__(self) -> None:
        import matplotlib
        self.plotstatus = matplotlib.get_backend()
        pass

    def trio_plt(self,qmean,qcum,quantiles): # 画收益图
        import matplotlib.pyplot as plt
        qmean[list(range(1,quantiles+1))].plot(kind= 'bar',title = 'mean')
        plt.show()
        qcum[list(range(1,quantiles+1))].plot(title = 'cumreturn')
        plt.legend(loc = 'upper center',bbox_to_anchor=(1.1, 1.02))
        plt.show()
        (qcum[10]-qcum[1]).plot(title = 'long-short')
        plt.show()

    def fbplot(self,frontplot,bgplot,c,fname,bname):
        # frontplot,bgplot:
        # pd.Series
        # multiindex: timestamp,code
        import matplotlib.pyplot as plt
        import matplotlib.ticker as ticker
        tickspace = len(frontplot)//12
        fig = plt.figure()
        a1=fig.add_axes([0,0,1,1])
        a1.bar(frontplot.index,bgplot.loc[frontplot.index],color = c)
        a1.tick_params(axis='x', labelrotation= 30)
        a1.xaxis.set_major_locator(ticker.MultipleLocator(tickspace))

        a2 = a1.twinx()
        a2.plot(frontplot.index,frontplot,color = 'red')
        a2.tick_params(axis='x', labelrotation= 30)
        a2.xaxis.set_major_locator(ticker.MultipleLocator(tickspace))
        

        fig.legend(frameon = False,labels = [bname+'(left)',fname+'(right)'],loc = 'upper center')
        plt.show()

    def factor_plt(self,qreturn,to,ictable,fc,ndays,savedir=''):
        from alphalens import utils
        from pandas.plotting import  table
        numtable = pd.concat([qreturn.mean(),qreturn.sum(),qreturn.mean()/qreturn.std()],axis = 1).rename(columns= {0:'avg',1:'sum',2:'risk-adj'}).T
        top_quantile = max(list(qreturn))
        totalSeed = qreturn.index
        xticks = list(range(0, len(totalSeed), 60))
        xlabels = [str(totalSeed[x]) for x in xticks]
        import matplotlib.pyplot as plt
        plt.figure(dpi=300, figsize=(24, 12))

        ax = plt.subplot(321,frame_on=False,title = fc+'_retsheet_bygroup')
        ax.xaxis.set_visible(False)  # hide the x axis
        ax.yaxis.set_visible(False)  # hide the y axis
        table(ax, numtable.round(5), loc='center')  # 将df换成需要保存的dataframe即可

        ax = plt.subplot(365,frame_on=False,title = str(ndays)+'days_information')
        ax.xaxis.set_visible(False)  # hide the x axis
        ax.yaxis.set_visible(False)  # hide the y axis
        table(ax, ictable.round(5), loc='center')  # 将df换成需要保存的dataframe即可

        plt.subplot(325,title = fc+'_cumret_bygroup')
        plt.plot(qreturn.index,qreturn.cumsum(),label = list(qreturn))
        plt.legend()
        plt.xticks(rotation=90)
        plt.xticks(ticks=xticks, labels=xlabels)

        plt.subplot(324,title = fc+'_turnover_bygroup')
        plt.bar(to.index,to,color="blue")

        plt.subplot(323,title = fc+'_avgret_bygroup')
        plt.bar(qreturn.mean().index,qreturn.mean(),color="y")

        plt.subplot(326,title = fc+'_lsret_bygroup')
        plt.plot(qreturn.index,(qreturn[top_quantile]-qreturn[1]).cumsum(),color="g")
        plt.xticks(rotation=90)
        plt.xticks(ticks=xticks, labels=xlabels)
        try:
            os.remove(savedir+fc+'.jpg')
            print(fc+'.jpg'+' 旧文件删除')
        except:
            print(fc+'.jpg'+' 是新文件')
        plt.savefig(savedir+fc+'.jpg')
        
        if self.plotstatus != 'agg':
            plt.show()
        plt.close()

    # 热力图展示
    def ShowHeatMap(self,DataFrame,savedir='',triangle = True):
        import matplotlib.pyplot as plt
        import seaborn as sns
        f, ax = plt.subplots(figsize=(35, 15))
        ax.set_title('Wine GRA')
        # 设置展示一半，如果不需要注释掉mask即可
        if triangle:
            mask = np.zeros_like(DataFrame)
            mask[np.triu_indices_from(mask)] = True  # np.triu_indices 上三角矩阵
        
            with sns.axes_style("white"):
                sns.heatmap(DataFrame,
                            cmap="YlGnBu",
                            annot=True,
                            mask=mask,
                            )
        else :
            with sns.axes_style("white"):
                sns.heatmap(DataFrame,
                            cmap="YlGnBu",
                            annot=True,
                            )
        plt.savefig(savedir)
        if self.plotstatus != 'agg':
            plt.show()

    def combine_imgs_pdf(self,folder_path, pdf_file_path,idstname):
        import os
        from PIL import Image
        """
        合成文件夹下的所有图片为pdf
        Args:
            folder_path (str): 源文件夹
            pdf_file_path (str): 输出路径
        """
        files = os.listdir(folder_path)
        png_files = []
        sources = []
        for file in files:
            if 'png' in file or 'jpg' in file:
                png_files.append(folder_path + file)
        png_files.sort()
    
        for file in png_files:
            png_file = Image.open(file)
            png_file = png_file.convert("RGB")
            sources.append(png_file)
        sources[0].save(pdf_file_path+'{}.pdf'.format(idstname), "pdf", save_all=True, append_images=sources[1:],quality = 95)

class mate_alphalens(object):
    def __init__(self) -> None:
        pass

    def index_mate(self,factordata,price):
        fcdf = factordata.reset_index()
        fcdf['date'] = pd.to_datetime(fcdf['date'])
        fcdf = fcdf.rename(columns = {'symbol':'asset'}).set_index(['date','asset'])
        ptemp = price.copy()
        ptemp.index = pd.to_datetime(ptemp.index)
        return fcdf,ptemp
    
    def trans_ex_return(self,clean_factor,index_price,ret_col):
        from alphalens import utils
        index_price['factor'] = 1
        base_ret = utils.compute_forward_returns(index_price[['factor']],index_price['close'].unstack())
        base_ret = base_ret.droplevel('asset').reindex(clean_factor.index.get_level_values(0))
        base_ret['asset'] = clean_factor.index.get_level_values('asset')
        base_ret = base_ret.set_index(['asset'],append=True)
        df = clean_factor.copy()
        df[ret_col]= df[ret_col]-base_ret[ret_col]
        return df

class alert(object):
    def __init__(self,**file):
        if file:
            self.filename = file
        else:
            import sys
            self.filename = sys.argv[0]
        pass

    def finish_alert(self):
        import smtplib
        from email.mime.multipart import MIMEMultipart 
        from email.mime.text import MIMEText
        from email.header import Header
        # 1. 连接邮箱服务器
        con = smtplib.SMTP_SSL('smtp.qq.com', 465)
        # 2. 登录邮箱 
        con.login('448986334@qq.com', 'jwtjvrktevlobiag')
        # 2. 准备数据
        # 创建邮件对象
        msg = MIMEMultipart()
        # 设置邮件主题
        subject = Header('{}程序运行完毕'.format(self.filename), 'utf-8').encode() 
        msg['Subject'] = subject
        # 设置邮件发送者
        msg['From'] = '448986334@qq.com'
        # 设置邮件接受者
        msg['To'] = 'lee15850574744@outlook.com'
        # 添加⽂文字内容
        text = MIMEText('{}程序运行完毕'.format(self.filename), 'plain', 'utf-8') 
        msg.attach(text)
        # 3.发送邮件
        con.sendmail('448986334@qq.com', 'lee15850574744@outlook.com', msg.as_string()) 
        con.quit()
    
    def breakdown_alert(self):
        import smtplib
        from email.mime.multipart import MIMEMultipart 
        from email.mime.text import MIMEText
        from email.header import Header
        # 1. 连接邮箱服务器
        con = smtplib.SMTP_SSL('smtp.qq.com', 465)
        # 2. 登录邮箱 
        con.login('448986334@qq.com', 'jwtjvrktevlobiag')
        # 2. 准备数据
        # 创建邮件对象
        msg = MIMEMultipart()
        # 设置邮件主题
        subject = Header('{}程序运行失败'.format(self.filename), 'utf-8').encode() 
        msg['Subject'] = subject
        # 设置邮件发送者
        msg['From'] = '448986334@qq.com'
        # 设置邮件接受者
        msg['To'] = 'lee15850574744@outlook.com'
        # 添加⽂文字内容
        text = MIMEText('{}程序运行失败'.format(self.filename), 'plain', 'utf-8') 
        msg.attach(text)
        # 3.发送邮件
        con.sendmail('448986334@qq.com', 'lee15850574744@outlook.com', msg.as_string()) 
        con.quit()
# sst:

    # def noise_judge(self,qreturn,fc):
    #     from scipy import stats
    #     from statsmodels.stats.diagnostic import acorr_ljungbox
    #     # 因子判别
    #     lsret,groupmean,groupmean_diff,top_sharp = self.judge_material(qreturn,fc)
    #     '''
    #     检验:
    #     对两个都没通过的可能是噪声的因子做自相关性检验,因为0假设是有相关性,所以哪怕只有一点自相关性(123123)都可能不会被拒绝，所以被拒绝的基本上可认定为噪声
    #     '''
    #     t,p_lsret =stats.ttest_1samp(lsret,0,alternative='greater')
    #     t,p_groupmean = stats.ttest_1samp(groupmean_diff,0,alternative='greater')
    #     if p_groupmean>0.05 and p_lsret>0.05:
    #         print(fc+'可能是噪声;分组平均收益一阶差分p值{},多空收益p值{}'.format(p_groupmean,p_lsret))
    #         # ls_ljung = acorr_ljungbox(lsret.cumsum(), lags=[1,5,10,20])
    #         gmdf_ljung =  acorr_ljungbox(groupmean, lags=[1,5])
    #         if gmdf_ljung['lb_pvalue'].min()>=0.05:
    #             print(fc+'是噪声;分组平均收益自相关检验最小p值{}'.format(gmdf_ljung['lb_pvalue'].min()))
    #             return True
    #         else:
    #             print('无法判定'+fc+'是噪声;分组平均收益自相关检验最小p值{}'.format(gmdf_ljung['lb_pvalue'].min()))
    #     return False


    # def short_judge(self,qreturn,fc):
    #     from scipy import stats
    #     # 因子判别
    #     lsret,groupmean,groupmean_diff = self.judge_material(qreturn,fc)       
    #     '''
    #     检验:
    #     对两个都通过的是有用的因子
    #     '''
    #     maxquantile = max(list(lsret))
    #     top5 = groupmean_diff.iloc[-5:]
    #     bottom5 = groupmean_diff.iloc[:5]
    #     t,p_top5 = stats.ttest_1samp(top5,0,alternative='greater')
    #     t,p_bottom5 = stats.ttest_1samp(bottom5,0,alternative='greater')
    #     if p_top5>0.5 and p_bottom5<0.1 and (abs(groupmean.iloc[-1])<abs(groupmean.iloc[0])):
    #         print(fc+'是空头因子;top5组平均收益一阶差分p值{},bottom5组平均收益一阶差分p值{}'.format(p_top5,p_bottom5))
    #         return True
    #     return False       


# mft:
    # def multif_denoisies(self,noise_factors_list,allfactors,threshold):
    #     '''
    #     输入:
    #     因子矩阵,噪声因子

    #     输出:
    #     去噪后的因子
    #     '''
    #     if len(noise_factors_list)==0:
    #         print('无可用于去噪的噪声')
    #         return allfactors
    #     other_factors_df = allfactors[list(filter(lambda x: x not in noise_factors_list,list(allfactors)))]
    #     noise_factors_df = self.ts_mat_orthog(allfactors[noise_factors_list])
    #     factordf = pd.concat([other_factors_df,noise_factors_df],axis = 1)
    #     # 去噪
    #     other_factors = list(other_factors_df)
    #     corrdf = self.multif_corr_ana(factordf,list(factordf))[0]
    #     print('相关性详情：')
    #     print(corrdf)
    #     corrdf = corrdf.loc[other_factors,noise_factors_list].abs().max(axis = 1)
    #     print('要被去噪的因子：')
    #     corr_with_noise = list(corrdf[corrdf>=threshold].index)
    #     print(corr_with_noise)
    #     for fc in corr_with_noise:
    #         factordf[fc] = self.orthog(factordf, fc, noise_factors_list)[0]
    #     return factordf[other_factors]

    
    # def multif_cal_weight(self,factordf,factorlist,return_col,weight_type):
    #     # factordf: pd.DataFrame
    #     # multiindex: timestamp,code
    #     # columns: factorname1, factorname2...,returndata
    #     # factorlist: strlist
    #     # return_col: column name, str
    #     df = factordf.copy()
    #     ret_k = self.fators_abnormal_ret(df,return_col,factorlist)
    #     ic = df.groupby(level = 'date').apply(lambda x: x.corr(method= 'spearman')[return_col])
    #     del ic['ret']
    #     weight = ret_k*ic
    #     direc = ic.mean().apply(lambda x: 1 if x>0 else -1)
    #     if weight_type == 1:
    #         return weight.mean()/weight.std()*direc
    #     elif weight_type == 2:
    #         return weight.mean()*direc
    #     else:
    #         return direc
    #     # if weight_type == '风险平价加权':
    #     #     cov = weight[factorlist].cov()
    #     #     from scipy.optimize import minimize
    #     #     def objective(x):
    #     #         w_cov = np.dot(cov,x.T)
    #     #         for n in range(len(x)):
    #     #             w_cov[n] *= x[n]
    #     #         mat = np.array([w_cov]*len(x))
    #     #         scale = 1/sum(abs(mat))
    #     #         return np.sum(abs(scale*(mat-mat.T)))
    #     #     initial_w=np.array([0.2]*len(factorlist))
    #     #     cons = []
    #     #     cons.append({'type':'eq','fun':lambda x: sum(x)-1})
    #     #     for i in range(len(initial_w)):
    #     #         cons.append({'type':'ineq','fun':lambda x: x[i]})
    #     #     #结果
    #     #     res=minimize(objective,initial_w,method='SLSQP',constraints=cons)
    #     #     params = pd.Series(res.x)
    #     #     params.index = cov.index
    #     #     return params

    # def weighted_factor(self,factordf,weight):
    #     # factordf: pd.DataFrame
    #     # multiindex: timestamp,code
    #     # columns: factorname1, factorname2...
    #     # weight:pd.Series
    #     wf = (weight*factordf).sum(axis = 1)

    #     return pd.DataFrame(wf,columns = ['weighted_factor'])