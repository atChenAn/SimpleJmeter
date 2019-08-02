import React from 'react';
import {Form, Input, Select} from 'antd';
import {FormWrapper, FiltersFormType} from 'search-page';
import SectionDatePicker from 'common/src/components/DatePicker';

const {Option} = Select;
const FilterForm: FiltersFormType = props => {
    const {
        form: {getFieldDecorator},
    } = props;

    return (
        <FormWrapper {...props} simpleMode={{rows: 1}}>
            ##REPLACE_FORM_CONTENT##
        </FormWrapper>
    );
};

export default FilterForm;
