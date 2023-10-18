import { i18nStrings } from '../constants/i18n';
import { Arn } from '../utils/ArnUtils';

const widgetStrings = i18nStrings.TableLabels;

interface RowData {
  name?: string;
  id?: number;
  status?: {
    state: string;
    timeline: {
      creationDateTime: string;
    };
  };
  clusterArn?: string;
}

const GetColumnConfig = () => {
  const columnConfig = [
    {
      dataKey: 'name',
      label: widgetStrings.name,
      disableSort: true,
      cellRenderer: ({ row: rowData }: { row: RowData }) => {
        const length = rowData.name?.length || 0;
        if (length > 20) {
          return rowData?.name?.slice(0, 19) + '...';
        }
        return rowData?.name;
      },
    },
    {
      dataKey: 'id',
      label: widgetStrings.id,
      disableSort: true,
      cellRenderer: ({ row: rowData }: { row: RowData }) => rowData?.id,
    },
    {
      dataKey: 'status',
      label: widgetStrings.status,
      disableSort: true,
      cellRenderer: ({ row: rowData }: { row: RowData }) => rowData?.status?.state, // TODO: Add icons for status
    },
    {
      dataKey: 'creationDateTime',
      label: widgetStrings.creationTime,
      disableSort: true,
      cellRenderer: ({ row: rowData }: { row: RowData }) => rowData?.status?.timeline.creationDateTime,
    },
    {
      dataKey: 'clusterArn',
      label: widgetStrings.accountId,
      disableSort: true,
      cellRenderer: ({ row: rowData }: { row: RowData }) => {
        if (rowData?.clusterArn) {
          return Arn.fromArnString(rowData.clusterArn).accountId;
        }
        return;
      },
    },
  ];
  return columnConfig;
};

export { GetColumnConfig };
