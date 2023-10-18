import React from 'react';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { ClusterDetails } from '../ClusterDetails';
import { i18nStrings } from '../../../../constants/i18n';

const expandClusterStrings = i18nStrings.Clusters.expandCluster;

describe('ClusterDetails', () => {
  it('renders component with provided props', () => {
    const clusterData = {
      cluster: {
        tags: [
          { key: 'Tag1', value: 'Value1' },
          { key: 'Tag2', value: 'Value2' },
        ],
      },
    };

    const instanceGroupData = [];

    const { getByText } = render(
      <ClusterDetails
        selectedClusterId="clusterId"
        accountId="accountId"
        clusterArn="clusterArn"
        clusterData={clusterData}
        instanceGroupData={instanceGroupData}
      />,
    );

    expect(getByText(expandClusterStrings.Overview)).toBeInTheDocument();
    expect(getByText(expandClusterStrings.ApplicationUserInterface)).toBeInTheDocument();
    expect(getByText(expandClusterStrings.Tags)).toBeInTheDocument();
  });
});
