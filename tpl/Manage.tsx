import React from 'react';
import createSearchPage, {GetDataApi} from 'search-page';
import {cloneDeep} from 'lodash';
import {apiname as API} from 'common/src/api';
import {notificationPop, NotificationType} from 'common/src/components';
import {GlobalErrorMsg} from 'common/src/constantValue/errorMessage.val';
import {getErrorMsg} from 'common/src/utils/commonUtils';
import FiltersForm from './FilterForm';
import Content from './Content';

const getDataApi: GetDataApi = async (filters, pagination) => {
    try {
        const filterDump = cloneDeep(filters);
        const {data} = await API.apiname({
            params: {
                ...filterDump,
                pageNo: pagination.current,
                pageSize: pagination.pageSize
            },
        });
        return {data, total: data.meta.totalCount};
    } catch (e) {
        notificationPop(NotificationType.ERROR, GlobalErrorMsg.ERROR_TITLE, getErrorMsg(e));
        return {
            data: [],
            total: 0,
        };
    }
};

const SearchPage = createSearchPage({
    getDataApi,
    FiltersForm,
});

const ContractComplated = props => {
    return (
        <SearchPage>
            {({data, forceUpdate}) => <Content data={data} forceUpdate={forceUpdate}/>}
        </SearchPage>
    );
};

export default ContractComplated;
