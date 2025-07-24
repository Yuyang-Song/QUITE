# Problem with a query in a Java Spring project using H2
[Link to question](https://stackoverflow.com/questions/56549963/problem-with-a-query-in-a-java-spring-project-using-h2)
**Creation Date:** 1560278562
**Score:** -3
**Tags:** spring, spring-boot, spring-mvc, spring-security, spring-data-jpa
## Question Body
<p>I have a project that uses H2 as the database and I'm trying to make a query of all users on it on my UserDAO, but when I try to run the terminal gives me a lot of errors and doesn't start the server, but when I comment the line of the query the program runs normally.</p>

<h1>ERROR</h1>

<pre><code>org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'loginController': Unsatisfied dependency expressed through field 'usuarioService'; nested exception is org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'usuarioService' defined in file [/home/gustavolbs/PSOFT/back-end/lab3/target/classes/com/lab2/crud/service/UsuarioService.class]: Unsatisfied dependency expressed through constructor parameter 0; nested exception is org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'userDAO': Invocation of init method failed; nested exception is java.lang.IllegalStateException: Using named parameters for method public abstract com.lab2.crud.model.User com.lab2.crud.dao.UserDAO.findByLogin(java.lang.String) but parameter 'Optional[searchLogin]' not found in annotated query 'Select u from User u where u.login=:plogin'!
</code></pre>

<h1>pom.xml</h1>

<pre><code>&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"&gt;
&lt;modelVersion&gt;4.0.0&lt;/modelVersion&gt;
&lt;parent&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-starter-parent&lt;/artifactId&gt;
    &lt;version&gt;2.1.5.RELEASE&lt;/version&gt;
    &lt;relativePath/&gt; &lt;!-- lookup parent from repository --&gt;
&lt;/parent&gt;
&lt;groupId&gt;com.lab2&lt;/groupId&gt;
&lt;artifactId&gt;crud&lt;/artifactId&gt;
&lt;version&gt;0.0.1-SNAPSHOT&lt;/version&gt;
&lt;name&gt;crud&lt;/name&gt;
&lt;description&gt;Demo project for Spring Boot&lt;/description&gt;

&lt;properties&gt;
    &lt;java.version&gt;1.8&lt;/java.version&gt;
&lt;/properties&gt;

&lt;dependencies&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
        &lt;artifactId&gt;spring-boot-starter-data-jpa&lt;/artifactId&gt;
    &lt;/dependency&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
        &lt;artifactId&gt;spring-boot-starter-web&lt;/artifactId&gt;
    &lt;/dependency&gt;

    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
        &lt;artifactId&gt;spring-boot-devtools&lt;/artifactId&gt;
        &lt;scope&gt;runtime&lt;/scope&gt;
    &lt;/dependency&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;com.h2database&lt;/groupId&gt;
        &lt;artifactId&gt;h2&lt;/artifactId&gt;
        &lt;scope&gt;runtime&lt;/scope&gt;
    &lt;/dependency&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
        &lt;artifactId&gt;spring-boot-starter-test&lt;/artifactId&gt;
        &lt;scope&gt;test&lt;/scope&gt;
    &lt;/dependency&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
        &lt;artifactId&gt;spring-boot-starter-thymeleaf&lt;/artifactId&gt;
    &lt;/dependency&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.projectlombok&lt;/groupId&gt;
        &lt;artifactId&gt;lombok&lt;/artifactId&gt;
        &lt;version&gt;1.18.4&lt;/version&gt;
        &lt;scope&gt;provided&lt;/scope&gt;
    &lt;/dependency&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;io.jsonwebtoken&lt;/groupId&gt;
        &lt;artifactId&gt;jjwt&lt;/artifactId&gt;
        &lt;version&gt;0.9.0&lt;/version&gt;
    &lt;/dependency&gt;
&lt;/dependencies&gt;

&lt;build&gt;
    &lt;plugins&gt;
        &lt;plugin&gt;
            &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
            &lt;artifactId&gt;spring-boot-maven-plugin&lt;/artifactId&gt;
        &lt;/plugin&gt;
    &lt;/plugins&gt;
&lt;/build&gt;
</code></pre>

<p></p>

<h1>Login Controller</h1>

<pre><code>package com.lab2.crud.controller;

import java.util.Date;

import javax.servlet.ServletException;

import com.lab2.crud.model.User;
import com.lab2.crud.service.UsuarioService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;

@RestController
@RequestMapping("/v1/auth")
public class LoginController {

    private final String TOKEN_KEY = "banana";

    @Autowired
    private UsuarioService usuarioService;

    @PostMapping("/login")
    public LoginResponse authenticate(@RequestBody User usuario) throws ServletException {

    // Recupera o usuario
    User authUsuario = usuarioService.findByLogin(usuario.getLogin());

    // verificacoes
    if(authUsuario == null) {
        throw new ServletException("Usuario nao encontrado!");
    }

    if(!authUsuario.getPassword().equals(usuario.getPassword())) {
        throw new ServletException("Senha invalida!");
    }

    String token = Jwts.builder().
            setSubject(authUsuario.getLogin()).
            signWith(SignatureAlgorithm.HS512, TOKEN_KEY).
            setExpiration(new Date(System.currentTimeMillis() + 1 * 60 * 1000))
            .compact();

        return new LoginResponse(token);


    }

    private class LoginResponse {
        public String token;

        public LoginResponse(String token) {
            this.token = token;
        }
    }

}
</code></pre>

<h1>UsuarioController</h1>

<pre><code>package com.lab2.crud.controller;

import com.lab2.crud.model.User;
import com.lab2.crud.service.UsuarioService;
import com.lab2.exception.Usuario.UsuarioJaExisteException;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;


@RestController
@RequestMapping("/v1/usuarios")
public class UsuarioController {

    @Autowired  
    private UsuarioService usuarioService;

    UsuarioController(UsuarioService usuarioService) {
        this.usuarioService = usuarioService;
    }

    @PostMapping(value="/")
    public ResponseEntity&lt;User&gt; create(@RequestBody User usuario) {

        if (usuarioService.findByLogin(usuario.getLogin()) != null) {
            throw new UsuarioJaExisteException("Usuário já existe");
        }

        User newUser = usuarioService.create(usuario);

        if (newUser == null) {
            throw new InternalError("Something went wrong");
        }

        return new ResponseEntity&lt;User&gt;(newUser, HttpStatus.CREATED);
    }

}
</code></pre>

<p>When I comment the line of the query on the UserDAO the program runs, but it doesn't do the search for the login.</p>

<h1>UserDAO</h1>

<pre><code>package com.lab2.crud.dao;

import java.io.Serializable;
import java.util.List;

import com.lab2.crud.model.User;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;


@Repository
public interface UserDAO&lt;T, ID extends Serializable&gt; extends JpaRepository&lt;User, String&gt; {

    User save(User usuario);
    User findById(long id);

    @Query("Select u from User u where u.login=:plogin")
    User findByLogin(@Param("searchLogin") String login);

    List&lt;User&gt; findAll();

}
</code></pre>

<h1>UserModel #</h1>

<pre><code>package com.lab2.crud.model;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

import lombok.Data;

@Data
@Entity
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long id;

    private String name;
    private String login;
    private String password;

    public User() {

    }

    public long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getLogin() {
        return login;
    }

    public String getPassword() {
        return password;
    }

    public User(String name, String login, String password) {
        this.name = name;
        this.login = login;
        this.password = password;
    }

}
</code></pre>

<h1>application.properties</h1>

<pre><code>server.port = 8080

# H2
spring.h2.console.enabled=true
spring.h2.console.path=/h2
#indicará o path para você acessar a interface do h2, em geral, vá ao browser e coloque localhost:8080/h2 com 8080 ou sua porta

# Datasource
spring.datasource.url=jdbc:h2:file:~/PSOFT/back-end/lab3/test
spring.datasource.username=sa
spring.datasource.password=
spring.datasource.driver-class-name=org.h2.Driver
spring.jpa.hibernate.ddl-auto=update

server.servlet.context-path=/api
#diz ao spring que coloque /api antes de qualquer url, ou seja, se voce quiser utilizar as rotas /products, precisará adicionar /api =&gt;  /api/v1/products e assim por diante
</code></pre>

<p>I've tried to rewrite the Query on another ways, tried re-import the package, run on another machine, but nothing works and I don't know what and why solve. Can anyone help me with this?</p>

## Answers
### Answer ID: 56550072
<p>In the DAO </p>

<pre><code>@Query("Select u from User u where u.login=:plogin")
User findByLogin(@Param("searchLogin") String login);
</code></pre>

<p>You have declared searchLogin as the parameter with @Param annotation but in the query you have used plogin as the parameter. Replace plogin with searchLogin in the query as shown below,</p>

<pre><code>@Query("Select u from User u where u.login=:searchLogin")
User findByLogin(@Param("searchLogin") String login);
</code></pre>

