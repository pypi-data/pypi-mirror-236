import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { pluginIds } from '../constants';

const ExamplePlugin: JupyterFrontEndPlugin<void> = {
  id: pluginIds.ExamplePlugin,
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    // implement your plugin here
  },
};

export { ExamplePlugin };
