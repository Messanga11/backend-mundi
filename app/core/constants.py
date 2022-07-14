from fastapi import HTTPException, status


class Constants:
    LOGIN_USER_ERROR= "LOGIN-USER-ERROR"
    LOGIN_PROVIDER_ERROR= "LOGIN-PROVIDER-ERROR"
    REGISTER_PROVIDER_ERROR= "REGISTER-PROVIDER-ERROR"
    REGISTER_USER_ERROR= "REGISTER-USER-ERROR"
    
    LOGIN_USER_EXCEPTION=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=LOGIN_USER_ERROR,
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    REGISTER_USER_EXCEPTION=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=REGISTER_USER_ERROR,
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    LOGIN_PROVIDER_EXCEPTION=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=LOGIN_PROVIDER_ERROR,
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    REGISTER_PROVIDER_EXCEPTION=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=REGISTER_PROVIDER_ERROR,
        headers={"WWW-Authenticate": "Bearer"},
    )