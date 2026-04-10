---
title: "Using @Transactional :: Spring Framework"
source: "https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html"
author:
published:
created: 2026-04-10
description:
tags:
  - "clippings"
---
In addition to the XML-based declarative approach to transaction configuration, you can use an annotation-based approach. Declaring transaction semantics directly in the Java source code puts the declarations much closer to the affected code. There is not much danger of undue coupling, because code that is meant to be used transactionally is almost always deployed that way anyway.

|     | The standard `jakarta.transaction.Transactional` annotation is also supported as a drop-in replacement for Spring’s own annotation. Please refer to the JTA documentation for more details. |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

The ease-of-use afforded by the use of the `@Transactional` annotation is best illustrated with an example, which is explained in the text that follows. Consider the following class definition:

- Java
- Kotlin

```java
// the service class that we want to make transactional
@Transactional
public class DefaultFooService implements FooService {

    @Override
    public Foo getFoo(String fooName) {
        // ...
    }

    @Override
    public Foo getFoo(String fooName, String barName) {
        // ...
    }

    @Override
    public void insertFoo(Foo foo) {
        // ...
    }

    @Override
    public void updateFoo(Foo foo) {
        // ...
    }
}
```

Used at the class level as above, the annotation indicates a default for all methods of the declaring class (as well as its subclasses). Alternatively, each method can be annotated individually. See [method visibility](#transaction-declarative-annotations-method-visibility) for further details on which methods Spring considers transactional. Note that a class-level annotation does not apply to ancestor classes up the class hierarchy; in such a scenario, inherited methods need to be locally redeclared in order to participate in a subclass-level annotation.

When a POJO class such as the one above is defined as a bean in a Spring context, you can make the bean instance transactional through an `@EnableTransactionManagement` annotation in a `@Configuration` class. See the [javadoc](https://docs.spring.io/spring-framework/docs/7.0.6/javadoc-api/org/springframework/transaction/annotation/EnableTransactionManagement.html) for full details.

The following example shows the configuration needed to enable annotation-driven transaction management:

- Java
- Kotlin
- Xml

```java
@Configuration
@EnableTransactionManagement
public class AppConfig {

    @Bean
    public FooService fooService() {
        return new DefaultFooService();
    }

    @Bean
    public PlatformTransactionManager txManager(DataSource dataSource) {
        return new DataSourceTransactionManager(dataSource);
    }
}
```

|  | In programmatic configuration, the `@EnableTransactionManagement` annotation uses any `TransactionManager` bean in the context. In XML configuration, you can omit the `transaction-manager` attribute in the `<tx:annotation-driven/>` tag if the bean name of the `TransactionManager` that you want to wire in has the name `transactionManager`. If the `TransactionManager` bean has any other name, you have to use the `transaction-manager` attribute explicitly, as in the preceding example. |
| --- | --- |

Reactive transactional methods use reactive return types in contrast to imperative programming arrangements as the following listing shows:

- Java
- Kotlin

```java
// the reactive service class that we want to make transactional
@Transactional
public class DefaultFooService implements FooService {

    @Override
    public Publisher<Foo> getFoo(String fooName) {
        // ...
    }

    @Override
    public Mono<Foo> getFoo(String fooName, String barName) {
        // ...
    }

    @Override
    public Mono<Void> insertFoo(Foo foo) {
        // ...
    }

    @Override
    public Mono<Void> updateFoo(Foo foo) {
        // ...
    }
}
```

Note that there are special considerations for the returned `Publisher` with regards to Reactive Streams cancellation signals. See the [Cancel Signals](https://docs.spring.io/spring-framework/reference/data-access/transaction/programmatic.html#tx-prog-operator-cancel) section under "Using the TransactionalOperator" for more details.

|     | Method visibility and `@Transactional` in proxy mode  The `@Transactional` annotation is typically used on methods with `public` visibility. As of 6.0, `protected` or package-visible methods can also be made transactional for class-based proxies by default. Note that transactional methods in interface-based proxies must always be `public` and defined in the proxied interface. For both kinds of proxies, only external method calls coming in through the proxy are intercepted.  If you prefer consistent treatment of method visibility across the different kinds of proxies (which was the default up until 5.3), consider specifying `publicMethodsOnly`:  ```java /**  * Register a custom AnnotationTransactionAttributeSource with the  * publicMethodsOnly flag set to true to consistently ignore non-public methods.  * @see ProxyTransactionManagementConfiguration#transactionAttributeSource()  */ @Bean TransactionAttributeSource transactionAttributeSource() {     return new AnnotationTransactionAttributeSource(true); } ```  The *Spring TestContext Framework* supports non-private `@Transactional` test methods by default as well. See [Transaction Management](https://docs.spring.io/spring-framework/reference/testing/testcontext-framework/tx.html) in the testing chapter for examples. |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |

You can apply the `@Transactional` annotation to an interface definition, a method on an interface, a class definition, or a method on a class. However, the mere presence of the `@Transactional` annotation is not enough to activate the transactional behavior. The `@Transactional` annotation is merely metadata that can be consumed by corresponding runtime infrastructure which uses that metadata to configure the appropriate beans with transactional behavior. In the preceding examples that use programmatic configuration, the `@EnableTransactionManagement` annotation switches on actual transaction management at runtime. Whereas, in the preceding example that uses XML configuration, the `<tx:annotation-driven/>` element switches on actual transaction management at runtime.

|     | The Spring team recommends that you annotate methods of concrete classes with the `@Transactional` annotation, rather than relying on annotated methods in interfaces, even if the latter does work for interface-based and target-class proxies as of 5.0. Since Java annotations are not inherited from interfaces, interface-declared annotations are still not recognized by the weaving infrastructure when using AspectJ mode, so the aspect does not get applied. As a consequence, your transaction annotations may be silently ignored: Your code might appear to "work" until you test a rollback scenario. |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

|  | In proxy mode (which is the default), only external method calls coming in through the proxy are intercepted. This means that self-invocation (in effect, a method within the target object calling another method of the target object) does not lead to an actual transaction at runtime even if the invoked method is marked with `@Transactional`. Also, the proxy must be fully initialized to provide the expected behavior, so you should not rely on this feature in your initialization code — for example, in a `@PostConstruct` method. |
| --- | --- |

Consider using AspectJ mode (see the `mode` attribute in the following table) if you expect self-invocations to be wrapped with transactions as well. In this case, there is no proxy in the first place. Instead, the target class is woven (that is, its byte code is modified) to support `@Transactional` runtime behavior on any kind of method.

| XML Attribute         | Annotation Attribute                                                                                                                                                                                  | Default                     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `transaction-manager` | N/A (see [`TransactionManagementConfigurer`](https://docs.spring.io/spring-framework/docs/7.0.6/javadoc-api/org/springframework/transaction/annotation/TransactionManagementConfigurer.html) javadoc) | `transactionManager`        | Name of the transaction manager to use. Required only if the name of the transaction manager is not `transactionManager`, as in the preceding example.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `mode`                | `mode`                                                                                                                                                                                                | `proxy`                     | The default mode (`proxy`) processes annotated beans to be proxied by using Spring’s AOP framework (following proxy semantics, as discussed earlier, applying to method calls coming in through the proxy only). The alternative mode (`aspectj`) instead weaves the affected classes with Spring’s AspectJ transaction aspect, modifying the target class byte code to apply to any kind of method call. AspectJ weaving requires `spring-aspects.jar` in the classpath as well as having load-time weaving (or compile-time weaving) enabled. (See [Spring configuration](https://docs.spring.io/spring-framework/reference/core/aop/using-aspectj.html#aop-aj-ltw-spring) for details on how to set up load-time weaving.) |
| `proxy-target-class`  | `proxyTargetClass`                                                                                                                                                                                    | `false`                     | Applies to `proxy` mode only. Controls what type of transactional proxies are created for classes annotated with the `@Transactional` annotation. If the `proxy-target-class` attribute is set to `true`, class-based proxies are created. If `proxy-target-class` is `false` or if the attribute is omitted, then standard JDK interface-based proxies are created. (See [Proxying Mechanisms](https://docs.spring.io/spring-framework/reference/core/aop/proxying.html) for a detailed examination of the different proxy types.)                                                                                                                                                                                           |
| `order`               | `order`                                                                                                                                                                                               | `Ordered.LOWEST_PRECEDENCE` | Defines the order of the transaction advice that is applied to beans annotated with `@Transactional`. (For more information about the rules related to ordering of AOP advice, see [Advice Ordering](https://docs.spring.io/spring-framework/reference/core/aop/ataspectj/advice.html#aop-ataspectj-advice-ordering).) No specified ordering means that the AOP subsystem determines the order of the advice.                                                                                                                                                                                                                                                                                                                 |

|  | The default advice mode for processing `@Transactional` annotations is `proxy`, which allows for interception of calls through the proxy only. Local calls within the same class cannot get intercepted that way. For a more advanced mode of interception, consider switching to `aspectj` mode in combination with compile-time or load-time weaving. |
| --- | --- |

|  | The `proxy-target-class` attribute controls what type of transactional proxies are created for classes annotated with the `@Transactional` annotation. If `proxy-target-class` is set to `true`, class-based proxies are created. If `proxy-target-class` is `false` or if the attribute is omitted, standard JDK interface-based proxies are created. (See [Proxying Mechanisms](https://docs.spring.io/spring-framework/reference/core/aop/proxying.html) for a discussion of the different proxy types.) |
| --- | --- |

|  | `@EnableTransactionManagement` and `<tx:annotation-driven/>` look for `@Transactional` only on beans in the same application context in which they are defined. This means that, if you put annotation-driven configuration in a `WebApplicationContext` for a `DispatcherServlet`, it checks for `@Transactional` beans only in your controllers and not in your services. See [MVC](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-servlet.html) for more information. |
| --- | --- |

The most derived location takes precedence when evaluating the transactional settings for a method. In the case of the following example, the `DefaultFooService` class is annotated at the class level with the settings for a read-only transaction, but the `@Transactional` annotation on the `updateFoo(Foo)` method in the same class takes precedence over the transactional settings defined at the class level.

- Java
- Kotlin

```java
@Transactional(readOnly = true)
public class DefaultFooService implements FooService {

    public Foo getFoo(String fooName) {
        // ...
    }

    // these settings have precedence for this method
    @Transactional(readOnly = false, propagation = Propagation.REQUIRES_NEW)
    public void updateFoo(Foo foo) {
        // ...
    }
}
```

## @Transactional Settings

The `@Transactional` annotation is metadata that specifies that an interface, class, or method must have transactional semantics (for example, "start a brand new read-only transaction when this method is invoked, suspending any existing transaction"). The default `@Transactional` settings are as follows:

- The propagation setting is `PROPAGATION_REQUIRED.`
- The isolation level is `ISOLATION_DEFAULT.`
- The transaction is read-write.
- The transaction timeout defaults to the default timeout of the underlying transaction system, or to none if timeouts are not supported.
- Any `RuntimeException` or `Error` triggers rollback, and any checked `Exception` does not.

You can change these default settings. The following table summarizes the various properties of the `@Transactional` annotation:

| Property | Type | Description |
| --- | --- | --- |
| [value](#tx-multiple-tx-mgrs-with-attransactional) | `String` | Optional qualifier that specifies the transaction manager to be used. |
| `transactionManager` | `String` | Alias for `value`. |
| `label` | Array of `String` labels to add an expressive description to the transaction. | Labels may be evaluated by transaction managers to associate implementation-specific behavior with the actual transaction. |
| [propagation](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/tx-propagation.html) | `enum`: `Propagation` | Optional propagation setting. |
| `isolation` | `enum`: `Isolation` | Optional isolation level. Applies only to propagation values of `REQUIRED` or `REQUIRES_NEW`. |
| `timeout` | `int` (in seconds of granularity) | Optional transaction timeout. Applies only to propagation values of `REQUIRED` or `REQUIRES_NEW`. |
| `timeoutString` | `String` (in seconds of granularity) | Alternative for specifying the `timeout` in seconds as a `String` value — for example, as a placeholder. |
| `readOnly` | `boolean` | Read-write versus read-only transaction. Only applicable to values of `REQUIRED` or `REQUIRES_NEW`. |
| `rollbackFor` | Array of `Class` objects, which must be derived from `Throwable.` | Optional array of exception types that must cause rollback. |
| `rollbackForClassName` | Array of exception name patterns. | Optional array of exception name patterns that must cause rollback. |
| `noRollbackFor` | Array of `Class` objects, which must be derived from `Throwable.` | Optional array of exception types that must not cause rollback. |
| `noRollbackForClassName` | Array of exception name patterns. | Optional array of exception name patterns that must not cause rollback. |

|  | See [Rollback rules](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/rolling-back.html#transaction-declarative-rollback-rules) for further details on rollback rule semantics, patterns, and warnings regarding possible unintentional matches for pattern-based rollback rules. |
| --- | --- |

|  | As of 6.2, you can globally change the default rollback behavior – for example, through `@EnableTransactionManagement(rollbackOn=ALL_EXCEPTIONS)`, leading to a rollback for all exceptions raised within a transaction, including any checked exception. For further customizations, `AnnotationTransactionAttributeSource` provides an `addDefaultRollbackRule(RollbackRuleAttribute)` method for custom default rules.  Note that transaction-specific rollback rules override the default behavior but retain the chosen default for unspecified exceptions. This is the case for Spring’s `@Transactional` as well as JTA’s `jakarta.transaction.Transactional` annotation.  Unless you rely on EJB-style business exceptions with commit behavior, it is advisable to switch to `ALL_EXCEPTIONS` for consistent rollback semantics even in case of a (potentially accidental) checked exception. Also, it is advisable to make that switch for Kotlin-based applications where there is no enforcement of checked exceptions at all. |
| --- | --- |

Currently, you cannot have explicit control over the name of a transaction, where 'name' means the transaction name that appears in a transaction monitor and in logging output. For declarative transactions, the transaction name is always the fully-qualified class name of the transactionally advised class + `.` + the method name. For example, if the `handlePayment(..)` method of the `BusinessService` class started a transaction, the name of the transaction would be `com.example.BusinessService.handlePayment`.

## Multiple Transaction Managers with @Transactional

Most Spring applications need only a single transaction manager, but there may be situations where you want multiple independent transaction managers in a single application. You can use the `value` or `transactionManager` attribute of the `@Transactional` annotation to optionally specify the identity of the `TransactionManager` to be used. This can either be the bean name or the qualifier value of the transaction manager bean. For example, using the qualifier notation, you can combine the following Java code with the following transaction manager bean declarations in the application context:

- Java
- Kotlin

```java
public class TransactionalService {

    @Transactional("order")
    public void setSomething(String name) { ... }

    @Transactional("account")
    public void doSomething() { ... }

    @Transactional("reactive-account")
    public Mono<Void> doSomethingReactive() { ... }
}
```

The following listing shows the bean declarations:

```xml
<tx:annotation-driven/>

    <bean id="transactionManager1" class="org.springframework.jdbc.support.JdbcTransactionManager">
        ...
        <qualifier value="order"/>
    </bean>

    <bean id="transactionManager2" class="org.springframework.jdbc.support.JdbcTransactionManager">
        ...
        <qualifier value="account"/>
    </bean>

    <bean id="transactionManager3" class="org.springframework.data.r2dbc.connection.R2dbcTransactionManager">
        ...
        <qualifier value="reactive-account"/>
    </bean>
```

In this case, the individual methods on `TransactionalService` run under separate transaction managers, differentiated by the `order`, `account`, and `reactive-account` qualifiers. The default `<tx:annotation-driven>` target bean name, `transactionManager`, is still used if no specifically qualified `TransactionManager` bean is found.

|  | If all transactional methods on the same class share the same qualifier, consider declaring a type-level `org.springframework.beans.factory.annotation.Qualifier` annotation instead. If its value matches the qualifier value (or bean name) of a specific transaction manager, that transaction manager is going to be used for transaction definitions without a specific qualifier on `@Transactional` itself.  Such a type-level qualifier can be declared on the concrete class, applying to transaction definitions from a base class as well. This effectively overrides the default transaction manager choice for any unqualified base class methods.  Last but not least, such a type-level bean qualifier can serve multiple purposes, for example, with a value of "order" it can be used for autowiring purposes (identifying the order repository) as well as transaction manager selection, as long as the target beans for autowiring as well as the associated transaction manager definitions declare the same qualifier value. Such a qualifier value only needs to be unique within a set of type-matching beans, not having to serve as an ID. |
| --- | --- |

## Custom Composed Annotations

If you find you repeatedly use the same attributes with `@Transactional` on many different methods, [Spring’s meta-annotation support](https://docs.spring.io/spring-framework/reference/core/beans/classpath-scanning.html#beans-meta-annotations) lets you define custom composed annotations for your specific use cases. For example, consider the following annotation definitions:

- Java
- Kotlin

```java
@Target({ElementType.METHOD, ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Transactional(transactionManager = "order", label = "causal-consistency")
public @interface OrderTx {
}

@Target({ElementType.METHOD, ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Transactional(transactionManager = "account", label = "retryable")
public @interface AccountTx {
}
```

The preceding annotations let us write the example from the previous section as follows:

- Java
- Kotlin

```java
public class TransactionalService {

    @OrderTx
    public void setSomething(String name) {
        // ...
    }

    @AccountTx
    public void doSomething() {
        // ...
    }
}
```

In the preceding example, we used the syntax to define the transaction manager qualifier and transactional labels, but we could also have included propagation behavior, rollback rules, timeouts, and other features.