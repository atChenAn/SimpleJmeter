<Form.Item label="##REPLACE_TITLE##">
    {getFieldDecorator('##REPLACE_KEY_NAME##', {})(
        <Select allowClear placeholder="##REPLACE_HINT##">
            <Option value="0">选项0</Option>
            <Option value="1">选项1</Option>
            <Option value="2">选项2</Option>
        </Select>
    )}
</Form.Item>