import React, { useState } from 'react';
import { SparkServerHistoryLink } from './SparkServerHistoryLink';
import { TezServerHistoryLink } from './TezServerHistoryLink';

import * as styles from './styles';
import { i18nStrings } from '../../../constants/i18n';

interface Props {
  selectedClusterId: string;
  clusterArn: string;
  accountId: string;
}

const expandClusterStrings = i18nStrings.Clusters.expandCluster;

const ClusterApplicationLinks: React.FunctionComponent<Props> = (props) => {
  const { accountId } = props;
  const [isError, setIsError] = useState(false);

  // TODO: Add any error handling if needed
  // TODO: Add conditions here along with isError to check if currentAppUIState is IDLE
  if (isError) {
    return <div>{expandClusterStrings.NotAvailable}</div>;
  }

  // TODO:: Update persistentAppUIId to be the id of the app UI that is created in the backend
  return (
    <>
      <div className={styles.Info}>
        <SparkServerHistoryLink accountId={accountId} persistentAppUIId={'persistentAppUIId'} setIsError={setIsError} />
      </div>
      <div className={styles.Info}>
        <TezServerHistoryLink accountId={accountId} persistentAppUIId={'persistentAppUIId'} setIsError={setIsError} />
      </div>
    </>
  );
};

export { ClusterApplicationLinks };
