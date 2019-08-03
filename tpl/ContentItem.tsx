<Column
    key="id"
    width="10%"
    title="###REPLACE_ITEM_TITLE##"
    render={(_, record: any) => <AutoText>{def(record.##REPLACE_ITEMKEY##)}</AutoText>}
/>