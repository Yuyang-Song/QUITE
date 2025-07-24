# .NET Core - Static classes, run from everywhere but still need DI and Entity Framework
[Link to question](https://stackoverflow.com/questions/56777127/net-core-static-classes-run-from-everywhere-but-still-need-di-and-entity-fra)
**Creation Date:** 1561565619
**Score:** 0
**Tags:** c#, asp.net-core, dependency-injection, singleton, static-classes
## Question Body
<p>Let me start by giving some code examples that are very common, very useful and used A LOT throughout the (web) application:</p>

<p><code>int? contactId = InfrastructureHelper.User.GetContactId()</code></p>

<p><code>int[] departmentIds = InfrastructureHelper.GetAuhthorizedDepartmentIds()</code></p>

<p><code>bool allowed = InfrastructureHelper.User.IsAllowedInPortal()</code></p>

<p><code>InfrastructureHelper.User.GetUserLanguage();</code></p>

<p>Just a few of some most used methods I call during the application life cycle.</p>

<p>While this all seems very cool and useful, it creates problem when used with Entity Framework and in a heavily async web application. Before in .NET Framework and with everything being synchronous (oh boy, those times), this was no problem. But now I am starting to see the problems and I need a solution.</p>

<p>Solution desires:</p>

<ul>
<li>Static if possible, to avoid injecting a class everywhere</li>
<li>It caches data for doing (additional) authorization checks (departments, controller-based authorization on top of the default role based authorization).</li>
<li>Thread-safe, because that's of course the problem now, I get the exception below here:</li>
</ul>

<blockquote>
  <p>System.InvalidOperationException: 'A second operation started on this context before a previous operation completed. This is usually caused by different threads using the same instance of DbContext, however instance members are not guaranteed to be thread safe. This could also be caused by a nested query being evaluated on the client, if this is the case rewrite the query avoiding nested invocations.'</p>
</blockquote>

<p>So I understand <a href="https://stackoverflow.com/questions/38138100/addtransient-addscoped-and-addsingleton-services-differences">how to use DI and the different possibilities</a>, I have <a href="https://stackoverflow.com/questions/45625745/how-to-handle-static-classes-running-in-the-same-context-scope-in-asp-net-core">seen other questions</a> that ask a similar question but the solution is working around the fact that I need a instance of Entity Framework injected.</p>

<p><code>InfrastructureHelper</code> holds a bunch of static members and 2 important interfaces, <code>ICurrentSession</code> and <code>ICurrentUser</code>. These interfaces are implemented differently per web application within the solution. The implementations are not static but do contain static members to cache some more data. <code>ICurrentSession</code> is not the problem here, that implementation of just injects <code>IHttpContextAccessor</code>. But <code>CurrentPortalUser</code> that implements <code>ICurrentUser</code> does inject repositories, let's give some code to read:</p>

<pre><code>public class CurrentPortalUser : ICurrentUser
{
    private readonly IUserRepository _userRepository;
    private readonly IControllerActionRepository _controllerActionRepository;
    private readonly IDepartmentRepository _departmentRepository;
    private static List&lt;DepartmentModel&gt; _allDepartments = new List&lt;DepartmentModel&gt;();
    private static List&lt;RoleModel&gt; _allRoles = new List&lt;RoleModel&gt;();
    private static List&lt;ControllerActionModel&gt; _allControllerActionRoles = new List&lt;ControllerActionModel&gt;();
    /// &lt;summary&gt;
    /// Simpler version of _allControllerActionRoles, Key: actionNamespace, Value: roleIds;
    /// &lt;/summary&gt;
    private static Dictionary&lt;string, string[]&gt; _allControllerActionRoleIds = new Dictionary&lt;string, string[]&gt;();

    /// &lt;summary&gt;
    /// Key: CountryId, Value: DepartmentId
    /// &lt;/summary&gt;
    private static Dictionary&lt;int, int&gt; _departmentCountryList = new Dictionary&lt;int, int&gt;();

    private readonly IHttpContextAccessor _httpContextAccessor;
    public CurrentPortalUser(IHttpContextAccessor httpContextAccessor, IUserRepository userRepository, IControllerActionRepository controllerActionRepository, IDepartmentRepository departmentRepository)
    {
        _httpContextAccessor = httpContextAccessor;
        _userRepository = userRepository;
        _controllerActionRepository = controllerActionRepository;
        _departmentRepository = departmentRepository;
    }

    public void ReloadDepartmentAndRoleData()
    {
        _allDepartments = _departmentRepository.GetAll().ToList();
        int[] departmentIds = _allDepartments.Select(x =&gt; x.DepartmentId).ToArray();
        List&lt;DepartmentCountryModel&gt; allDepartmentCountries = _departmentRepository.GetDepartmentOperatingCountries(departmentIds);
        _departmentCountryList = allWarehouseCountries.ToDictionary(x =&gt; x.CountryId, y =&gt; y.DepartmentId);

        //load role and controller configuration, basically tells me what role is allowed to execute what controller action within the web app.
        _allRoles = _userRepository.GetRoles().ToList();
        _allControllerActionRoles = _controllerActionRepository.GetAllWithRoles().ToList();
        _allControllerActionRoleIds = _allControllerActionRoles.ToDictionary(x =&gt; x.NameSpace.ToLower(), y =&gt; y.Roles.Select(z =&gt; z.RoleId).ToArray());

    }

    public List&lt;DepartmentModel&gt; GetAllowedDepartments()
    {
        if (!_allDepartments.Any())//store in memory, just like we are going to store all roles in memory
        {
            ReloadDepartmentAndRoleData();
        }
        if (!_allRoles.Any())
        {
            //load role and controller configuration
            ReloadDepartmentAndRoleData();
        }
        if (IsInRole(RoleEnum.SuperAdmin))
        {
            return _allDepartments;
        }
        List&lt;DepartmentModel&gt; allowedDepartments = new List&lt;DepartmentModel&gt;();
        foreach (DepartmentModel department in _allDepartments)
        {
            if (IsInRole(department.Name))
            {
                allowedDepartments.Add(department);
            }
        }
        return allowedDepartments;
    }

    public string GetUserId()
    {
        if (_httpContextAccessor.HttpContext.User.Identity.IsAuthenticated)
        {
            return _httpContextAccessor.HttpContext.User.FindFirst(ClaimTypes.Name)?.Value;
        }
        return null;
    }

    public int? GetContactId()
    {
        int? contactId = null;
        if (_httpContextAccessor.HttpContext.User.Identity.IsAuthenticated)
        {
            contactId = _userRepository.GetContactId(GetUserId());
        }
        return contactId;
    }
}
</code></pre>

<p>There is more to it, it basically comes down to obtain some data, if it's cached then get it from cache, else get it from the database and cache it or put it into session.</p>

<p>So now comes the part where I show you awful code which I am a bit embarrassed for :).</p>

<pre><code>public stattic class InfrastructureHelper
{
    //..more static members that are heavily used here, but these one are a bit-less depended on a database, as long as data can be obtained from IcurrentUser


    public static ICurrentUser User
    {
        get
        {
            return _container.GetInstance&lt;ICurrentUser&gt;();
        }
    }  

    //yup..that's static...
    private static ISimpleContainer _container;
    //this method is used via the Startup class, so only once
    public static void Initialize(ISimpleContainer container)
    {
        _container = container;
    }
}

//Since I don't have Asp.Net references in the project of InfrastructureHelper, I use a simple interface that of course does the same as the normal container
public interface ISimpleContainer
{
    TService GetInstance&lt;TService&gt;() where TService : class;
}
</code></pre>

<p>Last but not least, the registration of <code>ICurrentUser</code> is Transient (within Startup class)</p>

<pre><code>services.AddTransient&lt;ICurrentSession, CurrentPortalSession&gt;();
services.AddTransient&lt;ICurrentUser, CurrentPortalUser&gt;();
</code></pre>

<p>I get the reported exception at <code>InfrastructureHelper.User.GetContactId()</code>, because during or after login, it is used a lot at the same time. I could try to avoid that some requests are being executed at the same time or build a lock around that, but that just doesn't feel right.</p>

<p>Looking forward to your responses! Sorry of this is a very much of an anti-pattern, it's a piece of old code that has been easily copied to a new asp.net core environment without rechecking things because it's usability is so great :).</p>

<p><strong>Update</strong></p>

<p>So as per the comments, I was looking for a way to successfully inject the <code>InfrastructureHelper</code> everywhere. But when I try to inject this into every repository (make it part of the <code>BaseRepository</code>), then of course a circular  dependency will be detected: <code>ICurrentUser</code> is depended on some repositories, and every repository is depended on <code>InfrastructureHelper</code>(and thus <code>ICurrentUser</code>).</p>

