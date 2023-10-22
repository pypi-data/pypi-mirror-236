import { CommandRegistry } from '@lumino/commands';
import { UUID } from '../utils/uuid';
import { ActionAndLabelLike, BaseCommandArg, BaseInteraction } from './base';
import { castArgs } from '../utils/castArgs';

// Action
export type RenameColumnAction = BaseInteraction & {
  type: 'rename_column';
  previousColumnName: string;
  newColumnName: string;
};

// Action Creator
export function createRenameColumnActionAndLabelLike(
  previousColumnName: string,
  newColumnName: string
): ActionAndLabelLike<RenameColumnAction> {
  return {
    action: {
      id: UUID(),
      type: 'rename_column',
      previousColumnName,
      newColumnName
    },
    label: () => {
      return `Rename column ${previousColumnName} to ${newColumnName}`;
    }
  };
}

// Command
export type RenameColumnCommandArgs = BaseCommandArg & {
  previousColumnName: string;
  newColumnName: string;
};

// Command Option
export const renameColumnCommandOption: CommandRegistry.ICommandOptions = {
  execute(args) {
    const { cell, previousColumnName, newColumnName } =
      castArgs<RenameColumnCommandArgs>(args);

    const { action, label } = createRenameColumnActionAndLabelLike(
      previousColumnName,
      newColumnName
    );

    return cell.trrackManager.apply(action, label);
  },
  label: 'Rename Column'
};
