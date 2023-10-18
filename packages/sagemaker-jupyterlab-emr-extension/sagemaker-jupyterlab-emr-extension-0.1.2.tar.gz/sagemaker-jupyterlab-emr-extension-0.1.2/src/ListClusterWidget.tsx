import React, { Suspense } from 'react';
import { Dialog } from '@jupyterlab/apputils';
import { ListClusterView } from './components/ListClusterView';
import { HandleConnectType, ShowNotificationHandlerType } from './constants/types';

// @ts-ignore
class ListClusterWidget implements Dialog.IBodyWidget {
  readonly disposeDialog: any;
  readonly handleConnect: HandleConnectType;

  constructor(disposeDialog: ShowNotificationHandlerType, handleConnect: HandleConnectType) {
    this.disposeDialog = disposeDialog;
    this.handleConnect = handleConnect;
  }

  // TODO:: Add some fallback either spinner icon or some text is loading
  render() {
    return (
      <Suspense fallback={null}>
        <ListClusterView
          onCloseModal={this.disposeDialog}
          getConnectHandler={this.handleConnect}
          data-testid="list-cluster-view"
        />
      </Suspense>
    );
  }
}

const createListClusterWidget = (disposeDialog: () => void, handleConnect: HandleConnectType) =>
  new ListClusterWidget(disposeDialog, handleConnect);

export { createListClusterWidget };
