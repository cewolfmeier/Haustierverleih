import { useParams } from "react-router-dom";
import { useUser } from "../../contexts/UserContext";
import { useQuery } from "@tanstack/react-query";
import { usersQueries } from "../../services/users/queries";
import { rolesQueries } from "../../services/roles/types";

export default function EditUserPage(){
    const { userId } = useParams<{ userId: string }>();
    const { currentUser } = useUser();
    const { data:user, error, isFetching } = useQuery(usersQueries.byId(userId? userId:currentUser? currentUser.userId: 0));
    const { data:roles } = useQuery(rolesQueries.list());
    
    return(
        <>
            { user === undefined || isFetching?
                <p>Wird geladen...</p>
            :
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
                        {currentUser?.isAdmin &&
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
            }
        </>
    );
};