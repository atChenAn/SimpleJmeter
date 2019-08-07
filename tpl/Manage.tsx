import React from 'react';
import createSearchPage, {GetDataApi} from 'search-page';
import {cloneDeep} from 'lodash';
import { ##REPLACE_MANAGE_API## as API } from 'common/src/api';
import {notificationPop, NotificationType} from 'common/src/components';
import {GlobalErrorMsg} from 'common/src/constantValue/errorMessage.val';
import {getErrorMsg} from 'common/src/utils/commonUtils';
import FiltersForm from './FilterForm';
import Content from './Content';

const getDataApi: GetDataApi = async (filters, pagination) => {
    try {
        const filterDump = cloneDeep(filters);
        ##REPLACE_MANAGE_FILTER##
        const {data} = await API.##REPLACE_MANAGE_API_METHOD##({
            params: {
                ...filterDump,
                ##REPLACE_MANAGE_PAGE_NO##: pagination.current,
                ##REPLACE_MANAGE_PAGE_SIZE##: pagination.pageSize
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
