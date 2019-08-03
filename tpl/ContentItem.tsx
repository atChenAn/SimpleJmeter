<Column
    key="id"
    width="##REPLACE_ITEM_WIDTH##"
    title="##REPLACE_ITEM_TITLE##"
    render={(_, record: any) => <AutoText>{def(record.##REPLACE_ITEM_KEY##)}</AutoText>}
/>