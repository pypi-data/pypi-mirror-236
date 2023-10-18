import React from 'react';
import { i18nStrings } from '../../../constants/i18n';

import * as styles from './styles';

interface Props {
  accountId: string;
  persistentAppUIId: string;
  setIsError: (isError: boolean) => void;
}

const expandClusterStrings = i18nStrings.Clusters.expandCluster;

const TezServerHistoryLink: React.FunctionComponent<Props> = ({ accountId, persistentAppUIId, setIsError }) => {
  const [isLoading] = React.useState(false);
  const handleTezServerHistoryClick = () => {
    if (isLoading) {
      return;
    }

    // TODO: call API handler to create spark server history url and add error handling
  };

  return (
    <div className={styles.linkContainer} onClick={handleTezServerHistoryClick}>
      <div className={styles.link}>{expandClusterStrings.TezUI}</div>
      {isLoading && 'Loading...'}
    </div>
  );
};

export { TezServerHistoryLink };
