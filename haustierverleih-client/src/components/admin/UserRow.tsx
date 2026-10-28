import type { User } from "../../Schemas";

interface UserRowProps{
    user:User
}

export default function UserRow({user}:UserRowProps){
    return(
        <tr>
            <td>{user.username}</td>
            <td>{user.roleId.toString()}</td>
            <td>
                <a className="button" href="{{ url_for('admin.delete_user', user_id=user['user_id']) }}">Löschen</a>
                <a className="button" href="{{ url_for('admin.get_edit_user', user_id=user['user_id']) }}">Bearbeiten</a>
            </td>
        </tr>
    );
};