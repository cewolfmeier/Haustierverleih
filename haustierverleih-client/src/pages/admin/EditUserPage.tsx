import type { User, Role } from "../../Schemas";

interface EditUserPageProps{
    user:User,
    currentUser:User,
    roles:Role[],
}

export default function EditUserNamePage({user, currentUser, roles}:EditUserPageProps){
    const admin = {
        roleId: 1,
        role: "admin"
    }
    return(
        <>
            <h1>Benutzer { user.username } bearbeiten</h1>
            <div className="detail shadow">
                <form action="{{url_htmlFor('admin.post_edit_classNameName', classNameName_id=classNameName['classNameName_id'])}}" method="put">
                    {user === currentUser?
                        <>
                            <label htmlFor="current_password">Aktuelles Passwort</label>
                            <input type="password" name="current_password" id="current_password" required />
                            <label htmlFor="new_password">Neues Passwort</label>
                            <input type="password" name="new_password" id="new_password" required />
                            <label htmlFor="new_password_repeat">Neues Passwort wiederholen</label>
                            <input type="password" name="new_password_repeat" id="new_password_repeat" required />
                        </>
                        :
                        <>
                        {currentUser.roleId === admin.roleId &&
                            <>
                                <label htmlFor="roles">Benutzerrechte</label>
                                <select name="roles" id="roles" required>
                                    {roles.map(
                                        role=>(<option key={role.roleId} value={role.roleId} selected={user.roleId === role.roleId? true :false } >{role.role}</option>))}
                                </select>
                            </> 
                        }
                        </>
                    }
                    <input className="button-htmlForm" type="submit" value="Speichern" />
                </form>
            </div>
        </>
    );
};