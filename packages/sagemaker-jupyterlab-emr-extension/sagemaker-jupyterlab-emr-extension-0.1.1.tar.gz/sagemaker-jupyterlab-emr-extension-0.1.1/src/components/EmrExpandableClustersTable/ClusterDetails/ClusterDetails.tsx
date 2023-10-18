import React from 'react';
import { cx } from '@emotion/css';
import { i18nStrings } from '../../../constants/i18n';
import { ClusterTags } from './ClusterTags';
import { Cluster, ListInstanceGroupsOutput } from '../../../constants/types';
import {
  generateMasterNodesStringFromInstanceGroupData,
  generateApplicationsStringFromClusterData,
  generateCoreNodesStringFromInstanceGroupData,
} from '../../../utils/ClusterDetailUtils';
import { ClusterApplicationLinks } from '../ClusterApplicationLinks/ClusterApplicationLinks';
import * as styles from './styles';

interface Props {
  selectedClusterId: string;
  accountId: string;
  clusterArn: string;
  clusterData: Cluster | undefined;
  instanceGroupData: ListInstanceGroupsOutput | undefined;
}

const expandClusterStrings = i18nStrings.Clusters.expandCluster;

const ClusterDetails: React.FunctionComponent<Props> = ({
  clusterArn,
  accountId,
  selectedClusterId,
  clusterData,
  instanceGroupData,
}) => {
  // TODO: Uncomment and add code to pass data from API handlers
  const cluster = clusterData;
  const instanceGroupsData = instanceGroupData;
  return (
    <>
      <div className={styles.InformationContainer}>
        <h3>{expandClusterStrings.Overview}</h3>
        <div className={styles.Info}>{generateMasterNodesStringFromInstanceGroupData(instanceGroupsData)}</div>
        <div className={styles.Info}>{generateCoreNodesStringFromInstanceGroupData(instanceGroupsData)}</div>
        <div className={styles.Info}>
          {expandClusterStrings.Apps}: {generateApplicationsStringFromClusterData(cluster)}
        </div>
      </div>
      <div className={cx(styles.InformationContainer, styles.LinksContainer)}>
        <h3>{expandClusterStrings.ApplicationUserInterface}</h3>
        <ClusterApplicationLinks selectedClusterId={selectedClusterId} accountId={accountId} clusterArn={clusterArn} />
      </div>
      <div className={styles.InformationContainer}>
        <h3>{expandClusterStrings.Tags}</h3>
        <ClusterTags clusterData={clusterData} />
      </div>
    </>
  );
};

export { ClusterDetails, Props };
