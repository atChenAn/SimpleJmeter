/* eslint-disable jsx-a11y/no-static-element-interactions */

import React from 'react';
import {Table} from 'antd';
import styled from 'styled-components';
import {def} from 'common/src/utils/commonUtils';
import {AutoText} from 'common/src/components/AutoText/AutoText';

const Layout = styled.div``;
const {Column} = Table;

interface Props {
    data: Array<any>;
    forceUpdate?: () => void;
}

const Content = (props: Props) => {
    const {data, forceUpdate} = props;

    return (
        <Layout>
            <Table dataSource={data} pagination={false} rowKey="id">
                ##REPLACE_CONTENT_ITEMS##
            </Table>
        </Layout>
    );
};

export default Content;
