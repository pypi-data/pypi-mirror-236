"use strict";(self.webpackChunk_amzn_sagemaker_jupyterlab_emr_extension=self.webpackChunk_amzn_sagemaker_jupyterlab_emr_extension||[]).push([[232],{2232:(e,t,n)=>{n.r(t),n.d(t,{default:()=>Le});var o=n(3408),a=n(6029),l=n.n(a),r=n(2861),s=n(1837);const c="SelectedCell",i="HoveredCellClassname",d="SelectAuthContainer";var u;!function(e){e.emrConnect="sagemaker-studio:emr-connect"}(u||(u={}));const p={widgetTitle:"Connect to cluster",connectCommand:{label:"Connect",caption:"Connect to a cluster"},connectMessage:{errorTitle:"Error connecting to EMR cluster",successTitle:"Successfully connected to EMR cluster",errorDefaultMessage:"Error connecting to EMR cluster",successDefaultMessage:"Connected to EMR Cluster"},widgetConnected:"The notebook is connected to",defaultTooltip:"Select a cluster to connect to",widgetHeader:"Select a cluster to connect to. A code block will be added to the active cell and run automatically to establish the connection.",connectedWidgetHeader:"cluster. You can submit new jobs to run on the cluster.",connectButton:"Connect",learnMore:"Learn more",noResultsMatchingFilters:"There are no clusters matching the filter.",radioButtonLabels:{basicAccess:"Http basic authentication",noCredential:"No credential"},listClusterError:"Fail to list clusters, refresh the modal or try again later",noCluster:"No clusters are available",selectAuthTitle:"Select credential type for ",clusterButtonLabel:"Cluster",expandCluster:{MasterNodes:"Master nodes",CoreNodes:"Core nodes",NotAvailable:"Not available",NoTags:"No tags",SparkHistoryServer:"Spark History Server",TezUI:"Tez UI",Overview:"Overview",Apps:"Apps",ApplicationUserInterface:"Application user Interface",Tags:"Tags"}},m="Cancel",h=({handleClick:e,tooltip:t})=>l().createElement("div",{className:"EmrClusterContainer"},l().createElement(r.ToolbarButtonComponent,{className:"EmrClusterButton",tooltip:t,label:p.clusterButtonLabel,onClick:e,enabled:!0}));var g;!function(e){e.tab="Tab",e.enter="Enter",e.escape="Escape",e.arrowDown="ArrowDown"}(g||(g={}));var v=n(8278),b=n(1800),x=n(8564);const C={ModalBase:s.css`
  &.jp-Dialog {
    z-index: 1; /* Override default z-index so Dropdown menu is above the Modal */
  }
  .jp-Dialog-body {
    padding: var(--jp-padding-xl);
    .no-cluster-msg {
      padding: var(--jp-cell-collapser-min-height);
    }
  }
`,Header:s.css`
  width: 100%;
  display: contents;
  font-size: 0.5rem;
  h1 {
    margin: 0;
  }
`,HeaderButtons:s.css`
  display: flex;
  float: right;
`,ModalFooter:s.css`
  display: flex;
  justify-content: flex-end;
  background-color: var(--jp-layout-color2);
  padding: 12px 24px 12px 24px;
  button {
    margin: 5px;
  }
`,Footer:s.css`
  .jp-Dialog-footer {
    background-color: var(--jp-layout-color2);
    margin: 0;
  }
`,DismissButton:s.css`
  padding: 0;
  border: none;
  cursor: pointer;
`},f=({heading:e,headingId:t="modalHeading",className:n,shouldDisplayCloseButton:o=!1,onClickCloseButton:a,actionButtons:r})=>{let c=null,i=null;return o&&(c=l().createElement(v.z,{className:(0,s.cx)(C.DismissButton,"dismiss-button"),role:"button","aria-label":"close",onClick:a,"data-testid":"close-button"},l().createElement(b.closeIcon.react,{tag:"span"}))),r&&(i=r.map((e=>{const{className:t,component:n,onClick:o,label:a}=e;return n?l().createElement("div",{key:`${(0,x.v4)()}`},n):l().createElement(v.z,{className:t,type:"button",role:"button",onClick:o,"aria-label":a,key:`${(0,x.v4)()}`},a)}))),l().createElement("header",{className:(0,s.cx)(C.Header,n)},l().createElement("h1",{id:t},e),l().createElement("div",{className:(0,s.cx)(C.HeaderButtons,"header-btns")},i,c))};var y=n(6489);const E=({onCloseModal:e,onConnect:t,disabled:n})=>l().createElement("footer",{className:C.ModalFooter},l().createElement(v.z,{className:"jp-Dialog-button jp-mod-reject jp-mod-styled listcluster-cancel-btn",type:"button",onClick:e},m),l().createElement(v.z,{className:"jp-Dialog-button jp-mod-accept jp-mod-styled listcluster-connect-btn",type:"button",onClick:t,disabled:n},p.connectButton));class w{constructor(e="",t="",n="",o="",a="",l="",r=""){this.partition=e,this.service=t,this.region=n,this.accountId=o,this.resourceInfo=a,this.resourceType=l,this.resourceName=r}static getResourceInfo(e){const t=e.match(w.SPLIT_RESOURCE_INFO_REG_EXP);let n="",o="";return t&&(1===t.length?o=t[1]:(n=t[1],o=t[2])),{resourceType:n,resourceName:o}}static fromArnString(e){const t=e.match(w.ARN_REG_EXP);if(!t)throw new Error(`Invalid ARN format: ${e}`);const[,n,o,a,l,r]=t,{resourceType:s="",resourceName:c=""}=r?w.getResourceInfo(r):{};return new w(n,o,a,l,r,s,c)}static isValid(e){return!!e.match(w.ARN_REG_EXP)}static getArn(e,t,n,o,a,l){return`arn:${e}:${t}:${n}:${o}:${a}/${l}`}}w.ARN_REG_EXP=/^arn:(.*?):(.*?):(.*?):(.*?):(.*)$/,w.SPLIT_RESOURCE_INFO_REG_EXP=/^(.*?)[/:](.*)$/,w.VERSION_DELIMITER="/";const k={name:"Name",id:"ID",status:"Status",creationTime:"Creation Time",createdOn:"Created On",accountId:"Account ID"};var I=n(2510),N=n(4321);s.css`
  height: 100%;
  position: relative;
`;const S=s.css`
  margin-right: 10px;
`,_=(s.css`
  ${S}
  svg {
    width: 6px;
  }
`,s.css`
  background-color: var(--jp-layout-color2);
  label: ${i};
  cursor: pointer;
`),T=s.css`
  background-color: var(--jp-layout-color3);
  -webkit-touch-callout: none; /* iOS Safari */
  -webkit-user-select: none; /* Safari */
  -khtml-user-select: none; /* Konqueror HTML */
  -moz-user-select: none; /* Old versions of Firefox */
  -ms-user-select: none; /* Internet Explorer/Edge */
  user-select: none; /* Non-prefixed version, currently supported by Chrome, Opera and Firefox */
  label: ${c};
`,R=s.css`
  background-color: var(--jp-layout-color2);
  display: flex;
  padding: var(--jp-cell-padding);
  width: 100%;
  align-items: baseline;
  justify-content: start;
  /* box shadow */
  -moz-box-shadow: inset 0 -15px 15px -15px var(--jp-layout-color3);
  -webkit-box-shadow: inset 0 -15px 15px -15px var(--jp-layout-color3);
  box-shadow: inset 0 -15px 15px -15px var(--jp-layout-color3);
  /* Disable visuals for scroll */
  overflow-x: scroll;
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
  &::-webkit-scrollbar {
    display: none;
  }
`,j={borderTop:"var(--jp-border-width) solid var(--jp-border-color1)",borderBottom:"var(--jp-border-width) solid var(--jp-border-color1)",borderRight:"var(--jp-border-width) solid var(--jp-border-color1)",display:"flex",boxSizing:"border-box",marginRight:"0px",padding:"2.5px",fontWeight:"initial",textTransform:"capitalize",color:"var(--jp-ui-font-color2)"},A={display:"flex",flexDirection:"column",height:"max-content"},M=s.css`
  display: flex;
`,D={height:"max-content",display:"flex",overflow:"auto",padding:"var(--jp-cell-padding)"},$=({isSelected:e})=>e?l().createElement(b.caretDownIcon.react,{tag:"span"}):l().createElement(b.caretRightIcon.react,{tag:"span"}),B=({dataList:e,tableConfig:t,selectedId:n,expandedView:o,noResultsView:r,showIcon:c,isLoading:i,columnConfig:d,onRowSelect:u,...p})=>{const m=(0,a.useRef)(null),h=(0,a.useRef)(null),[g,v]=(0,a.useState)(-1),[b,x]=(0,a.useState)(0);(0,a.useEffect)((()=>{var e,t;x((null===(e=null==h?void 0:h.current)||void 0===e?void 0:e.clientHeight)||28),null===(t=m.current)||void 0===t||t.recomputeRowHeights()}),[n,i,t.width,t.height]);const C=({rowData:e,...t})=>e?(0,I.defaultTableCellDataGetter)({rowData:e,...t}):null;return l().createElement(I.Table,{...p,...t,headerStyle:j,ref:m,headerHeight:28,rowCount:e.length,rowData:e,noRowsRenderer:()=>r,rowHeight:({index:t})=>e[t].id&&e[t].id===n?b:28,rowRenderer:e=>{const{style:t,key:a,rowData:r,index:c,className:i}=e,d=n===r.id,u=g===c,p=(0,s.cx)(M,i,{[T]:d,[_]:!d&&u});return d?l().createElement("div",{key:a,ref:h,style:{...t,...A},onMouseEnter:()=>v(c),onMouseLeave:()=>v(-1),className:p},(0,N.Cx)({...e,style:{width:t.width,...D}}),l().createElement("div",{className:R},o)):l().createElement("div",{key:a,onMouseEnter:()=>v(c),onMouseLeave:()=>v(-1)},(0,N.Cx)({...e,className:p}))},onRowClick:({rowData:e})=>u(e),rowGetter:({index:t})=>e[t]},d.map((({dataKey:t,label:o,disableSort:a,cellRenderer:r})=>l().createElement(I.Column,{key:t,dataKey:t,label:o,flexGrow:1,width:150,disableSort:a,cellDataGetter:C,cellRenderer:t=>((t,o)=>{const{rowIndex:a,columnIndex:r}=t,s=e[a].id===n,i=0===r;let d=null;return o&&(d=o({row:e[a],rowIndex:a,columnIndex:r,onCellSizeChange:()=>null})),i&&c?l().createElement(l().Fragment,null,l().createElement($,{isSelected:s})," ",d):d})(t,r)}))))},L=s.css`
  height: 100%;
  position: relative;
`,z=s.css`
  margin-right: 10px;
`,H=(s.css`
  ${z}
  svg {
    width: 6px;
  }
`,s.css`
  text-align: center;
  margin: 0;
  position: absolute;
  top: 50%;
  left: 50%;
  margin-right: -50%;
  transform: translate(-50%, -50%);
`),O=(s.css`
  background-color: var(--jp-layout-color2);
  label: ${i};
  cursor: pointer;
`,s.css`
  background-color: var(--jp-layout-color3);
  -webkit-touch-callout: none; /* iOS Safari */
  -webkit-user-select: none; /* Safari */
  -khtml-user-select: none; /* Konqueror HTML */
  -moz-user-select: none; /* Old versions of Firefox */
  -ms-user-select: none; /* Internet Explorer/Edge */
  user-select: none; /* Non-prefixed version, currently supported by Chrome, Opera and Firefox */
  label: ${c};
`,s.css`
  background-color: var(--jp-layout-color2);
  display: flex;
  padding: var(--jp-cell-padding);
  width: 100%;
  align-items: baseline;
  justify-content: start;

  /* box shadow */
  -moz-box-shadow: inset 0 -15px 15px -15px var(--jp-layout-color3);
  -webkit-box-shadow: inset 0 -15px 15px -15px var(--jp-layout-color3);
  box-shadow: inset 0 -15px 15px -15px var(--jp-layout-color3);

  /* Disable visuals for scroll */
  overflow-x: scroll;
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
  &::-webkit-scrollbar {
    display: none;
  }
`,s.css`
  padding: 24px 24px 12px 24px;
`),F=s.css`
  .ReactVirtualized__Table__headerRow {
    display: flex;
  }
  .ReactVirtualized__Table__row {
    display: flex;
    margin: var(--jp-cell-padding);
    font-size: 12px;
  }
`,G=s.css`
  display: flex;
`,P=(s.css`
  width: 100%;
  overflow-x: scroll;
  display: flex;
  flex-direction: row;
`,s.css`
  flex-direction: column;
  margin: 0 32px 8px 8px;
  flex: 1 0 auto;
  width: 33%;
`),U=s.css`
  width: 20%;
`,V=s.css`
  margin-bottom: var(--jp-code-padding);
`,K=p.expandCluster,W=({clusterData:e})=>{const t=null==e?void 0:e.tags;return(null==t?void 0:t.length)?l().createElement(l().Fragment,null,t.map((e=>l().createElement("div",{className:V,key:null==e?void 0:e.key},null==e?void 0:e.key,": ",null==e?void 0:e.value)))):l().createElement("div",null,K.NoTags)},X=p.expandCluster,q=s.css`
  cursor: pointer;
  & {
    color: var(--jl-content-link-color);
    text-decoration: none;
    text-underline-offset: 1.5px;
    text-decoration: underline;

    &:hover:not([disabled]) {
      text-decoration: underline;
    }

    &:focus:not([disabled]) {
      border: var(--jl-border-width) solid var(--jl-brand-color2);
    }

    &:active:not([disabled]) {
      text-decoration: underline;
    }

    &[disabled] {
      color: var(--jl-ui-font-color3);
    }
  }
`,J=s.css`
  display: flex;
`,Z=(s.css`
  margin-left: 10px;
`,s.css`
  margin-bottom: var(--jp-code-padding);
`),Y=p.expandCluster,Q=({persistentAppUIId:e,accountId:t,setIsError:n})=>{const[o]=l().useState(!1);return l().createElement("div",{className:J,onClick:()=>{o||n(!1)}},l().createElement("div",{className:(0,s.cx)("HistoryLink",q)},Y.SparkHistoryServer),o&&"Loading...")},ee=p.expandCluster,te=({accountId:e,persistentAppUIId:t,setIsError:n})=>{const[o]=l().useState(!1);return l().createElement("div",{className:J,onClick:()=>{}},l().createElement("div",{className:q},ee.TezUI),o&&"Loading...")},ne=p.expandCluster,oe=e=>{const{accountId:t}=e,[n,o]=(0,a.useState)(!1);return n?l().createElement("div",null,ne.NotAvailable):l().createElement(l().Fragment,null,l().createElement("div",{className:Z},l().createElement(Q,{accountId:t,persistentAppUIId:"persistentAppUIId",setIsError:o})),l().createElement("div",{className:Z},l().createElement(te,{accountId:t,persistentAppUIId:"persistentAppUIId",setIsError:o})))},ae=p.expandCluster,le=({clusterArn:e,accountId:t,selectedClusterId:n,clusterData:o,instanceGroupData:a})=>{const r=o,c=a;return l().createElement(l().Fragment,null,l().createElement("div",{className:P},l().createElement("h3",null,ae.Overview),l().createElement("div",{className:V},(e=>{var t;const n=null===(t=null==e?void 0:e.instanceGroups)||void 0===t?void 0:t.find((e=>"MASTER"===(null==e?void 0:e.instanceGroupType)));if(n){const e=n.runningInstanceCount,t=n.instanceType;return`${X.MasterNodes}: ${e}, ${t}`}return`${X.MasterNodes}: ${X.NotAvailable}`})(c)),l().createElement("div",{className:V},(e=>{var t;const n=null===(t=null==e?void 0:e.instanceGroups)||void 0===t?void 0:t.find((e=>"CORE"===(null==e?void 0:e.instanceGroupType)));if(n){const e=n.runningInstanceCount,t=n.instanceType;return`${X.CoreNodes}: ${e}, ${t}`}return`${X.CoreNodes}: ${X.NotAvailable}`})(c)),l().createElement("div",{className:V},ae.Apps,": ",(e=>{const t=null==e?void 0:e.applications;return(null==t?void 0:t.length)?t.map(((e,n)=>{const o=n===t.length-1?".":", ";return`${null==e?void 0:e.name} ${null==e?void 0:e.version}${o}`})):`${X.NotAvailable}`})(r))),l().createElement("div",{className:(0,s.cx)(P,U)},l().createElement("h3",null,ae.ApplicationUserInterface),l().createElement(oe,{selectedClusterId:n,accountId:t,clusterArn:e})),l().createElement("div",{className:P},l().createElement("h3",null,ae.Tags),l().createElement(W,{clusterData:o})))},re=p,se=l().createElement("div",{className:L},l().createElement("p",{className:H},re.noResultsMatchingFilters)),ce=({clustersList:e,tableConfig:t,clusterManagementListConfig:n,selectedClusterId:o,clusterArn:a,accountId:r,onRowSelect:s,clusterDetails:c,...i})=>{const d=!c&&!1,u=c;return l().createElement(B,{...i,tableConfig:t,showIcon:!0,dataList:e,selectedId:o,columnConfig:n,isLoading:d,noResultsView:se,onRowSelect:s,expandedView:d?l().createElement("span",{className:G},l().createElement(y.Z,null)):l().createElement(le,{selectedClusterId:o,accountId:r||"",clusterArn:a,clusterData:u,instanceGroupData:void 0})})};n(7960);const ie=[200,201];var de,ue=n(4788),pe=n(4614);!function(e){e.POST="POST",e.GET="GET",e.PUT="PUT"}(de||(de={}));const me=async(e,t,n)=>{const o=ue.ServerConnection.makeSettings(),a=pe.URLExt.join(o.baseUrl,e);try{const e=await ue.ServerConnection.makeRequest(a,{method:t,body:n},o);if(!ie.includes(e.status))throw new Error("Unable to fetch data");return e.json()}catch(e){return e}},he={width:850,height:500},ge=e=>{const{onCloseModal:t,getConnectHandler:n}=e,[o,r]=(0,a.useState)([]),[c,i]=(0,a.useState)(!1),[d,u]=(0,a.useState)(""),[m,h]=(0,a.useState)(void 0),[g,v]=(0,a.useState)(),[b,x]=(0,a.useState)(""),[C,f]=(0,a.useState)(!0),I=[{dataKey:"name",label:k.name,disableSort:!0,cellRenderer:({row:e})=>{var t,n;return((null===(t=e.name)||void 0===t?void 0:t.length)||0)>20?(null===(n=null==e?void 0:e.name)||void 0===n?void 0:n.slice(0,19))+"...":null==e?void 0:e.name}},{dataKey:"id",label:k.id,disableSort:!0,cellRenderer:({row:e})=>null==e?void 0:e.id},{dataKey:"status",label:k.status,disableSort:!0,cellRenderer:({row:e})=>{var t;return null===(t=null==e?void 0:e.status)||void 0===t?void 0:t.state}},{dataKey:"creationDateTime",label:k.creationTime,disableSort:!0,cellRenderer:({row:e})=>{var t;return null===(t=null==e?void 0:e.status)||void 0===t?void 0:t.timeline.creationDateTime}},{dataKey:"clusterArn",label:k.accountId,disableSort:!0,cellRenderer:({row:e})=>{if(null==e?void 0:e.clusterArn)return w.fromArnString(e.clusterArn).accountId}}],N=async(e="")=>{try{i(!0);const t=JSON.stringify({ClusterStates:["RUNNING","WAITING"],...e&&{Marker:e}}),n=await me("/aws/sagemaker/api/emr/list-clusters",de.POST,t);r((e=>[...e,...n.clusters])),(null==n?void 0:n.Marker)?N(null==n?void 0:n.Marker):i(!1)}catch(e){i(!1),u(e)}};(0,a.useEffect)((()=>{N()}),[]),(0,a.useEffect)((()=>{g&&h((async e=>{const t=JSON.stringify({ClusterId:e}),n=await me("/aws/sagemaker/api/emr/describe-cluster",de.POST,t);h(n.cluster)})(g))}),[g]);const S=(0,a.useMemo)((()=>null==o?void 0:o.sort(((e,t)=>{const n=e.name,o=t.name;return null==n?void 0:n.localeCompare(o)}))),[o]),_=(0,a.useCallback)((e=>{const t=S.find((t=>t.id===e));let n="";const o=null==t?void 0:t.clusterArn;return o&&w.isValid(o)&&(n=w.fromArnString(o).accountId),o&&(n=b),n}),[S]),T=(0,a.useCallback)((e=>{const t=S.find((t=>t.id===e)),n=null==t?void 0:t.clusterArn;return n&&w.isValid(n)?n:""}),[S]),R=(0,a.useCallback)((e=>{const t=null==e?void 0:e.id;t&&t===g?(v(t),x(""),f(!0)):(v(t),x(_(t)),f(!1))}),[g,_]);return l().createElement(l().Fragment,null,d&&l().createElement("span",null,d),c?l().createElement("span",{className:G},l().createElement(y.Z,null)):(j=o,Array.isArray(j)&&j.length>0?l().createElement("div",{className:(0,s.cx)(O,"modal-body-container")},l().createElement(l().Fragment,null,l().createElement("div",{className:(0,s.cx)(F,"grid-wrapper")},l().createElement(ce,{clustersList:S,selectedClusterId:null!=g?g:"",clusterArn:T(null!=g?g:""),accountId:_(null!=g?g:""),tableConfig:he,clusterManagementListConfig:I,onRowSelect:R,clusterDetails:m})))):l().createElement("div",{className:"no-cluster-msg"},p.noCluster)),l().createElement(E,{onCloseModal:t,onConnect:()=>{n(t,m)()},disabled:C}));var j};class ve{constructor(e,t){this.disposeDialog=e,this.handleConnect=t}render(){return l().createElement(a.Suspense,{fallback:null},l().createElement(ge,{onCloseModal:this.disposeDialog,getConnectHandler:this.handleConnect,"data-testid":"list-cluster-view"}))}}const be=(e,t)=>new ve(e,t);var xe=n(1105);const Ce=s.css`
  h2 {
    font-size: var(--jl-ui-font-size1);
    margin-top: 0;
  }
`,fe=s.css`
  .DataGrid-ContextMenu > div {
    overflow: hidden;
  }
  margin: 12px;
`,ye=s.css`
  padding-bottom: 0;
`,Ee=s.css`
  background-color: var(--jp-layout-color2);
  display: flex;
  justify-content: flex-end;
  button {
    margin: 5px;
  }
`,we=s.css`
  text-align: center;
  vertical-align: middle;
`,ke={ModalBase:Ce,ModalBody:fe,ModalFooter:Ee,ListTable:s.css`
  overflow: hidden;
`,NoHorizontalPadding:s.css`
  padding-left: 0;
  padding-right: 0;
`,RadioGroup:s.css`
  display: flex;
  justify-content: flex-start;
  li {
    margin-right: 20px;
  }
`,ModalHeader:ye,ModalMessage:we,AuthModal:s.css`
  min-height: none;
`,ListClusterModal:s.css`
  /* so the modal height remains the same visually during and after loading (this number can be changed) */
  min-height: 600px;
`,ConnectCluster:s.css`
  white-space: nowrap;
`,ClusterDescription:s.css`
  display: inline;
`,PresignedURL:s.css`
  line-height: normal;
`,ClusterListModalCrossAccountError:s.css`
  display: flex;
  flex-direction: column;
  padding: 0 0 10px 0;
`,GridWrapper:s.css`
  box-sizing: border-box;
  width: 100%;
  height: 100%;

  & .ReactVirtualized__Grid {
    /* important is required because react virtualized puts overflow style inline */
    overflow-x: hidden !important;
  }

  & .ReactVirtualized__Table__headerRow {
    display: flex;
  }

  & .ReactVirtualized__Table__row {
    display: flex;
    margin: var(--jp-cell-padding);
    font-size: 12px;
  }
`,EmrExecutionRoleContainer:s.css`
  margin-top: 25px;
  width: 90%;
`,Dropdown:s.css`
  margin-top: var(--jp-cell-padding);
`},Ie=({onCloseModal:e,getConnectHandler:t,selectedCluster:n,notebookPanel:o})=>{const r=`${d}`,c=`${d}`,[i,u]=(0,a.useState)("Basic_Access"),m=(0,a.useMemo)((()=>t(e,n,i,void 0,o)),[t,e,n,i,o]);return l().createElement("div",{className:(0,s.cx)(r,ke.ModalBase,ke.AuthModal)},l().createElement("div",{className:(0,s.cx)(c,ke.ModalBody)},l().createElement(xe.FormControl,null,l().createElement(xe.RadioGroup,{"aria-labelledby":"demo-radio-buttons-group-label",defaultValue:"Basic_Access",value:i,onChange:e=>{"Basic_Access"!==e.target.value&&"None"!==e.target.value||u(e.target.value)},name:"radio-buttons-group","data-testid":"radio-button-group",row:!0},l().createElement(xe.FormControlLabel,{value:"Basic_Access",control:l().createElement(xe.Radio,null),label:p.radioButtonLabels.basicAccess}),l().createElement(xe.FormControlLabel,{value:"None",control:l().createElement(xe.Radio,null),label:p.radioButtonLabels.noCredential})))),l().createElement(E,{onCloseModal:e,onConnect:m,disabled:!1}))};class Ne{constructor(e,t,n,o){this.disposeDialog=e,this.handleConnect=t,this.selectedCluster=n,this.notebookPanel=o}render(){return l().createElement(Ie,{onCloseModal:this.disposeDialog,getConnectHandler:this.handleConnect,selectedCluster:this.selectedCluster,notebookPanel:this.notebookPanel})}}const Se=(e,t,n,o)=>new Ne(e,t,n,o),_e=(e,t,n)=>{t.execute(e,n)},Te=e=>t=>n=>{_e(e,t,n)},Re=Object.fromEntries(Object.entries(u).map((e=>{const t=e[0],n=e[1];return[t,(o=n,{id:o,createRegistryWrapper:Te(o),execute:(e,t)=>_e(o,e,t)})];var o}))),je=s.css`
  .jp-Dialog-content {
    width: 900px;
    max-width: none;
    max-height: none;
    padding: 0;
  }
  .jp-Dialog-header {
    padding: 24px 24px 12px 24px;
    background-color: var(--jp-layout-color2);
  }
  /* Hide jp footer so we can add custom footer with button controls. */
  .jp-Dialog-footer {
    display: none;
  }
`;class Ae extends r.ReactWidget{constructor(e,t){super(),this._setSelectedCluster=e=>{var t;(null===(t=this._selectedCluster)||void 0===t?void 0:t.id)!==e.id&&(this._selectedCluster=e)},this.updateConnectedCluster=e=>{this._connectedCluster=e,this.update()},this.getToolTip=()=>this._connectedCluster?`${p.widgetConnected} ${this._connectedCluster.name} cluster`:p.defaultTooltip,this.openSelectAuthType=async e=>{let t={};const n=()=>t&&t.resolve();t=new r.Dialog({title:l().createElement(f,{heading:`${p.selectAuthTitle}"${e.name}"`,shouldDisplayCloseButton:!0,onClickCloseButton:n}),body:Se(n,this.handleConnect,e).render()}),t.addClass((0,s.cx)(C.ModalBase,C.Footer,je)),t.launch()},this.handleConnect=(e,t,n)=>()=>{if(!t)return;this._setSelectedCluster(t);const o=n||((null===(l=(a=t).kerberosAttributes)||void 0===l?void 0:l.kdcAdminPassword)?"Kerberos":(null===(r=a.configurations)||void 0===r?void 0:r.some((e=>{var t;return"ldap"===(null===(t=null==e?void 0:e.properties)||void 0===t?void 0:t.livyServerAuthType)})))?"Basic_Access":null);var a,l,r;o?(e(),this._appContext.commands.execute(Re.emrConnect.id,{clusterId:t.id,authType:o,language:"python"})):(e(),this.openSelectAuthType(t))},this.clickHandler=async()=>{let e={};const t=()=>e&&e.resolve();e=new r.Dialog({title:l().createElement(f,{heading:p.widgetTitle,shouldDisplayCloseButton:!0,onClickCloseButton:t,className:"list-cluster-modal-header"}),body:be(t,this.handleConnect).render()}),e.handleEvent=t=>{"keydown"===t.type&&(({keyboardEvent:e,onEscape:t,onShiftTab:n,onShiftEnter:o,onTab:a,onEnter:l})=>{const{key:r,shiftKey:s}=e;s?r===g.tab&&n?n():r===g.enter&&o&&o():r===g.tab&&a?a():r===g.enter&&l?l():r===g.escape&&t&&t()})({keyboardEvent:t,onEscape:()=>e.reject()})},e.addClass((0,s.cx)(C.ModalBase,C.Footer,je)),e.launch()},this._selectedCluster=null,this._appContext=t,this._connectedCluster=null,this._kernelId=null}get kernelId(){return this._kernelId}get selectedCluster(){return this._selectedCluster}updateKernel(e){this._kernelId!==e&&(this._kernelId=e,this.kernelId&&this.update())}render(){return l().createElement(h,{handleClick:this.clickHandler,tooltip:p.defaultTooltip})}}const Me=e=>null!=e,De=p,$e={id:"@sagemaker-studio:EmrCluster",autoStart:!0,optional:[o.INotebookTracker],activate:async(e,t)=>{e.docRegistry.addWidgetExtension("Notebook",new Be(e)),e.commands.addCommand(Re.emrConnect.id,{label:e=>De.connectCommand.label,isEnabled:()=>!0,isVisible:()=>!0,caption:()=>De.connectCommand.caption,execute:async t=>{try{const{clusterId:n,authType:a,language:l,crossAccountArn:r,executionRoleArn:s,notebookPanelToInjectCommandInto:c}=t,i="%load_ext sagemaker_studio_analytics_extension.magics",d=Me(l)?`--language ${l}`:"",u=`${i}\n%sm_analytics emr connect --verify-certificate False --cluster-id ${n} --auth-type ${a} ${d} ${Me(r)?`--assumable-role-arn ${r}`:""} ${Me(s)?`--emr-execution-role-arn ${s}`:""}`,p=c||(e=>{const t=e.shell.widgets("main");let n=t.next().value;for(;n;){if(n.hasClass("jp-NotebookPanel")&&n.isVisible)return n;n=t.next().value}return null})(e);await(async(e,t,n=!0)=>new Promise((async(a,l)=>{if(t){const r=t.content,s=r.model,c=t.context.sessionContext,{metadata:i}=s.sharedModel.toJSON(),d={cell_type:"code",metadata:i,source:e},u=r.activeCell,p=u?r.activeCellIndex:0;if(s.sharedModel.insertCell(p,d),r.activeCellIndex=p,n)try{await o.NotebookActions.run(r,c)}catch(e){l(e)}const m=[];for(const e of u.outputArea.node.children)m.push(e.innerHTML);a({html:m,cell:u})}l("No notebook panel")})))(u,p)}catch(e){throw e.message,e}}})}};class Be{constructor(e){this.appContext=e}createNew(e,t){const n=(o=e.sessionContext,a=this.appContext,new Ae(o,a));var o,a;return e.context.sessionContext.kernelChanged.connect((e=>{var t;const o=null===(t=e.session)||void 0===t?void 0:t.kernel;e.iopubMessage.connect(((e,t)=>{((e,t,n,o)=>{if(n)try{if(e.content.text){const{isConnSuccess:t,clusterId:a}=(e=>{let t,n=!1;if(e.content.text){const o=JSON.parse(e.content.text);if("sagemaker-analytics"!==o.namespace)return{};t=o.cluster_id,n=o.success}return{isConnSuccess:n,clusterId:t}})(e);t&&n.id===a&&o(n)}}catch(e){return}})(t,0,n.selectedCluster,n.updateConnectedCluster)})),o&&o.spec.then((e=>{e&&e.metadata&&n.updateKernel(o.id)})),n.updateKernel(null)})),e.toolbar.insertBefore("kernelName","emrCluster",n),n}}const Le=[$e]}}]);